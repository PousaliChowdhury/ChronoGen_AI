import streamlit as st 
import pandas as pd
import random
import os
import base64

st.set_page_config(layout="wide")

def center_header(text):
    st.markdown(f"<h1 style='text-align: center;'>{text}</h1>", unsafe_allow_html=True)

def center_subheader(text):
    st.markdown(f"<h3 style='text-align: center; color: gray;'>{text}</h3>", unsafe_allow_html=True)

def set_background(image_path):
    if not os.path.isfile(image_path):
        return
    with open(image_path, "rb") as img_file:
        base64_img = base64.b64encode(img_file.read()).decode()
    st.markdown(f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpeg;base64,{base64_img}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        h1, h2, h3, label {{
            color: white !important;
            text-shadow: 1px 1px 2px #000;
        }}
        
        </style>
    """, unsafe_allow_html=True)

center_header("🔁LifeSync: Smart Routine Generator")
center_subheader("Design Your Day. Automate Your Focus.")

routine_type = st.selectbox("Select Routine Type", ["School", "University", "Gym/Training", "Home/Self-Study", "Work"])
bg_images = {
    "School": "images/school.jpg","University": "images/uni.jpg","Gym/Training": "images/gym.jpg","Home/Self-Study": "images/study.jpeg","Work": "images/work.jpeg",
}
set_background(bg_images.get(routine_type))
center_header(f"{routine_type} Routine")

class Data:
    def __init__(self):
        self.departments = {}
        self.rooms = []
        self.labs = []
        self.meeting_times = []

class Schedule:
    def __init__(self, data):
        self.data = data
        self.classes = []
        self.num_conflicts = 0
        self.fitness = -1
        self.initialize()

    def initialize(self):
        assigned_class_slots = set()
        for dept, details in self.data.departments.items():
            for course, students in details['courses']:
                instructors = details['course_teacher_map'].get(course, [])
                if not instructors:
                    continue
                instructor = random.choice(instructors)
                while True:
                    room = random.choice(self.data.rooms)
                    time = random.choice(self.data.meeting_times)
                    slot = (time, room)
                    if slot not in assigned_class_slots:
                        assigned_class_slots.add(slot)
                        self.classes.append({
                            "Department": dept,
                            "Course": course,
                            "Instructor": instructor,
                            "Time": time,
                            "Room": room,
                            "Students": students,
                            "Type": "Lecture"
                        })
                        break
        self.fitness = 1 / (1 + self.num_conflicts)

    def get_fitness(self):
        return self.fitness

class Population:
    def __init__(self, size, data):
        self.schedules = [Schedule(data) for _ in range(size)]
        for schedule in self.schedules:
            schedule.initialize()

    def get_schedules(self):
        return self.schedules

class GeneticAlgorithm:
    def evolve_population(self, pop):
        return Population(len(pop.get_schedules()), pop.get_schedules()[0].data)
    
departments = {}

if routine_type == "School":
    st.markdown("## 🏫 School Routine Setup")
    class_selected = st.selectbox("Select Class", list(range(1, 13)))
    is_senior = class_selected in [11, 12]
    entity_label = "Stream" if is_senior else "Section"

    col1, col2 = st.columns(2)

    with col1:
        num_entities = st.number_input(f"Number of {entity_label}s", 1, 10, 1)
    with col2:    
        entity_names = st.text_input(f"{entity_label} Names (comma-separated)",
                                 value=", ".join([f"{entity_label} {i+1}" for i in range(num_entities)]))
    departments_list = [e.strip() for e in entity_names.split(",")][:num_entities]

    entity_data = [
        {"name": ent, "students": st.number_input(f"Students in {ent}", 1, 100, 10, key=f"students_{ent}")}
        for ent in departments_list
    ]

    st.markdown("### 📚 Subjects and Teachers")
    col1, col2 = st.columns(2)
    with col1:    
        num_subjects = st.number_input("Number of Subjects", 1, 10, 1)
    with col2:    
        subject_list = st.text_input("Subject Names (comma-separated)",
                                 value=", ".join([f"Subj{i+1}" for i in range(num_subjects)])).split(",")[:num_subjects]
    subject_list = [s.strip() for s in subject_list]

    col1, col2 = st.columns(2)
    with col1: 
        num_teachers = st.number_input("Number of Teachers", 1, 15, 1)
    with col2: 
        teacher_list = st.text_input("Teacher Names (comma-separated)",
                                 value=", ".join([f"Teacher{i+1}" for i in range(num_teachers)])).split(",")[:num_teachers]
    teacher_list = [t.strip() for t in teacher_list]

    st.markdown("### 🧠 Assign Subjects to Teachers")
    teacher_subject_map = {teacher: st.multiselect(f"{teacher} teaches:", subject_list, key=f"{teacher}_subjects")
                           for teacher in teacher_list}

    departments = {
        ent["name"]: {
            "teachers": teacher_list,
            "courses": [(subj, ent["students"]) for subj in subject_list],
            "course_teacher_map": {
                subj: [t for t in teacher_list if subj in teacher_subject_map[t]]
                for subj in subject_list
            }
        } for ent in entity_data
    }


elif routine_type == "University":
    st.markdown("## 🎓 University Routine Setup")
    
    program = st.selectbox("Choose a University Program", [
        "B.Tech", "M.Tech", "B.Sc", "M.Sc", "BA", "MA", "BBA", "MBA"
    ])
    
    col1, col2 = st.columns(2)
    with col1:
        num_departments = st.number_input("Number of Departments", 1, 10, 1)
    with col2:
        department_names = st.text_input("Department Names (comma-separated)", 
                                         value=", ".join([f"Department {i+1}" for i in range(num_departments)]))
    departments_list = [dept.strip() for dept in department_names.split(",")][:num_departments]

    department_data = [
        {"name": dept, "students": st.number_input(f"Students in {dept}", 1, 300, 60, key=f"students_{dept}")}
        for dept in departments_list
    ]
    
    st.markdown("### 📚 Subjects and Professors")
    col1, col2 = st.columns(2)
    with col1:
        num_subjects = st.number_input("Number of Subjects", 1, 10, 1)
    with col2:
        subject_list = st.text_input("Subject Names (comma-separated)",
                                     value=", ".join([f"Subj{i+1}" for i in range(num_subjects)])).split(",")[:num_subjects]
    subject_list = [s.strip() for s in subject_list]

    col1, col2 = st.columns(2)
    with col1:
        num_professors = st.number_input("Number of Professors", 1, 15, 1)
    with col2:
        professor_list = st.text_input("Professor Names (comma-separated)",
                                       value=", ".join([f"Professor{i+1}" for i in range(num_professors)])).split(",")[:num_professors]
    professor_list = [t.strip() for t in professor_list]

    st.markdown("### 🧠 Assign Subjects to Professors")
    professor_subject_map = {professor: st.multiselect(f"{professor} teaches:", subject_list, key=f"{professor}_subjects")
                             for professor in professor_list}

    departments = {
        dept["name"]: {
            "teachers": professor_list,
            "courses": [(subj, dept["students"]) for subj in subject_list],
            "course_teacher_map": {
                subj: [t for t in professor_list if subj in professor_subject_map[t]]
                for subj in subject_list
            }
        } for dept in department_data
    }


if routine_type in ["School", "University"]:
    
    col1, col2 = st.columns(2)
    with col1:
        num_rooms = st.number_input("Number of Classrooms", 1, 10, 1, key="room_ct")
    with col2:
        room_names_input = st.text_input("Room Names (comma-separated)",
                                     value=", ".join([f"Room{i+1}" for i in range(num_rooms)]))

    rooms = [room.strip() for room in room_names_input.split(",")][:num_rooms]

    num_periods = st.number_input("Number of Periods per Day", min_value=1, max_value=10, value=1)

    meeting_times = [
        st.text_input(f"Period Slot {i+1}", key=f"time_{i}") for i in range(num_periods)]


elif routine_type == "Gym/Training":
    st.subheader("💪 Gym/Training Config")
    gcols = st.columns(4)

    num_trainers = gcols[0].number_input("Trainers", 1, 5, 2)
    num_trainees = gcols[1].number_input("Trainees", 1, 100, 10)
    trainees_per = gcols[2].number_input("Max per Trainer", 1, 20, 5)
    num_training_slots = gcols[3].number_input("Training Slots", 1, 5, 2)  # Use number_input here for slots

    num_trainers = int(num_trainers)
    num_trainees = int(num_trainees)
    trainees_per = int(trainees_per)
    num_training_slots = int(num_training_slots)

    trainers = [st.text_input(f"Trainer {i+1}", key=f"tr_{i}") for i in range(num_trainers)]
    training_slots = [st.text_input(f"Slot {i+1}", key=f"ts_{i}") for i in range(num_training_slots)]


elif routine_type == "Home/Self-Study":
    st.subheader("📚 Study Setup")
    gcols = st.columns(3)
    num_tasks = int(gcols[0].number_input("Resource", 1, 5, 1))
    num_breaks = int(gcols[1].number_input("Time Slots", 0, 100, 1))
    num_study = int(gcols[2].number_input("Study subjects", 1, 20, 1))

    study_times = [st.text_input(f"Study Subject {i+1}", key=f"study_{i}") for i in range(num_study)]
    task_times = [st.text_input(f"Resource {i+1}", key=f"task_{i}") for i in range(num_tasks)]
    break_times = [st.text_input(f"Study Time {i+1}", key=f"break_{i}") for i in range(num_breaks)]


elif routine_type == "Work":
    st.subheader("🧠 Work Mode")
    pcols = st.columns(2)
    num_projects = int(pcols[0].number_input("Projects", 1, 5, 1))
    num_sessions = int(pcols[1].number_input("Sessions", 1, 5, 1))

    projects = [st.text_input(f"Project {i+1}", key=f"prj_{i}") for i in range(num_projects)]
    work_sessions = [st.text_input(f"Session {i+1}", key=f"ws_{i}") for i in range(num_sessions)]



if st.button("📌 Generate Optimized Routine"):
    st.success("✅ Routine Generated")

    if routine_type in ["School", "University"]:
        data = Data()
        data.departments = departments
        data.rooms = rooms
        data.meeting_times = meeting_times

        pop = Population(10, data)
        ga = GeneticAlgorithm()
        for _ in range(100):
            pop = ga.evolve_population(pop)

        best = pop.get_schedules()[0]
        st.markdown(f"**Fitness Score:** `{best.get_fitness():.4f}`")
        header = f"Class: {class_selected}" if routine_type == "School" else f"Program: {program}"
        st.markdown(f"### 🗓️ {routine_type} Routine - {header}")
        st.dataframe(pd.DataFrame(best.classes))


    elif routine_type == "Gym/Training":
        st.dataframe(pd.DataFrame({"Trainer": trainers * len(training_slots),
                                   "Time Slot": training_slots * len(trainers)}))


    elif routine_type == "Home/Self-Study":
        max_len = max(len(task_times), len(study_times), len(break_times))

        task_times += [""] * (max_len - len(task_times))
        study_times += [""] * (max_len - len(study_times))
        break_times += [""] * (max_len - len(break_times))

        st.dataframe(pd.DataFrame({
            "Study Time": study_times,
            "Resource": task_times,
            "Break Time": break_times
        }))


    elif routine_type == "Work":
        st.dataframe(pd.DataFrame({
            "Project": projects,
            "Session": work_sessions + [""] * (len(projects) - len(work_sessions))
        }))
