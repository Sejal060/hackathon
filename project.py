"""
HackaAIverse - AI Agent-Based Hackathon Management System
Enhanced with Groq-powered intelligent agents
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json

# Import our custom modules
from config import Config, COMPETITION_CATEGORIES, HACKATHON_SCHEDULE
from data_manager import DataManager
from ai_agents import AgentFactory

# Initialize components
data_manager = DataManager()
config_validation = Config.validate_config()

# Initialize Firebase only if explicitly configured
firebase_db = None
if str(getattr(Config, "DATABASE_TYPE", "json")).lower() == "firebase":
    try:
        # Only attempt init if FIREBASE_KEY looks like a JSON object
        if Config.FIREBASE_KEY and Config.FIREBASE_KEY.strip().startswith("{"):
            import firebase_admin
            from firebase_admin import credentials, firestore

            if not getattr(firebase_admin, "_apps", []):
                import json
                key_dict = json.loads(Config.FIREBASE_KEY)
                cred = credentials.Certificate(key_dict)
                firebase_admin.initialize_app(cred)
            firebase_db = firestore.client()
        else:
            firebase_db = None
    except Exception:
        # Quietly fallback to None (JSON storage is default)
        firebase_db = None

# Initialize AI Agents
@st.cache_resource
def initialize_agents():
    """Initialize AI agents with caching"""
    return {
        "mentor": AgentFactory.create_mentor_bot(),
        "judging": AgentFactory.create_judging_bot(),
        "challenge_generator": AgentFactory.create_challenge_generator(),
        "reminder": AgentFactory.create_reminder_bot()
    }

# Page configuration
st.set_page_config(
    page_title="HackaAIverse 2025",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)


def display_system_status():
    """Display system configuration status"""
    st.sidebar.markdown("### 🔧 System Status")

    status_items = [
        ("Groq API", "✅" if config_validation["groq_api_key"] else "❌"),
        ("Data Directory", "✅" if config_validation["data_directory"] else "❌"),
        ("Email Config", "✅" if config_validation["email_config"] else "⚠️"),
    ]

    for item, status in status_items:
        st.sidebar.markdown(f"{status} {item}")

def home_page():
    """Enhanced home page with comprehensive features"""
    st.title(f"🚀 {Config.HACKATHON_NAME}")
    st.markdown(f"**Theme:** {Config.HACKATHON_THEME}")

    # Display event information
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Event Date", Config.EVENT_DATE)
    with col2:
        st.metric("Registration Deadline", Config.REGISTRATION_DEADLINE)
    with col3:
        stats = data_manager.get_statistics()
        st.metric("Registered Teams", stats["total_teams"])

    # Event Schedule
    st.header("📅 Event Schedule")
    schedule_df = pd.DataFrame([
        {"Time": time, "Activity": activity}
        for time, activity in HACKATHON_SCHEDULE.items()
    ])
    st.table(schedule_df)

    # Problem Statements
    st.header("💡 Problem Statements")
    problems = data_manager.get_problems()

    if not problems:
        st.info("No problem statements available yet.")
    else:
        # Filter by category
        categories = ["All"] + COMPETITION_CATEGORIES
        selected_category = st.selectbox("Filter by Category", categories)

        filtered_problems = problems
        if selected_category != "All":
            filtered_problems = [p for p in problems if p.get("category") == selected_category]

        for i, problem in enumerate(filtered_problems):
            with st.expander(f"🎯 {problem['title']} ({problem.get('category', 'General')})"):
                st.write(problem["description"])

                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Difficulty:** {problem.get('difficulty', 'Medium')}")
                with col2:
                    tech_stack = problem.get('tech_stack', [])
                    if tech_stack:
                        st.write(f"**Suggested Tech:** {', '.join(tech_stack)}")

def team_registration():
    """Enhanced team registration with validation"""
    st.header("👥 Team Registration")

    with st.form("register_team"):
        st.subheader("Team Information")
        team_name = st.text_input("Team Name*", help="Choose a unique team name")

        st.subheader("Team Members")
        member_count = st.number_input("Number of Members", min_value=1, max_value=6, value=3)
        members = []

        for i in range(member_count):
            member_name = st.text_input(f"Member {i+1} Name*")
            if member_name:
                members.append(member_name)

        st.subheader("Contact Information")
        email = st.text_input("Team Email*", help="Primary contact email")
        college = st.text_input("College/University*")
        contact_number = st.text_input("Contact Number")

        if st.form_submit_button("Register Team"):
            if not team_name or not members or not email or not college:
                st.error("Please fill in all required fields marked with *")
            else:
                try:
                    team_id = data_manager.register_team(
                        team_name=team_name,
                        members=members,
                        email=email,
                        college=college,
                        contact_number=contact_number
                    )
                    st.success(f"✅ Team '{team_name}' registered successfully! Team ID: {team_id}")

                    # Send welcome message using ReminderBot
                    agents = initialize_agents()
                    welcome_message = agents["reminder"].generate_reminder(
                        "registration_confirmation",
                        {"team_name": team_name, "event_name": Config.HACKATHON_NAME}
                    )
                    st.info(f"📧 Welcome Message: {welcome_message}")

                except ValueError as e:
                    st.error(f"Registration failed: {str(e)}")

def project_submission():
    """Enhanced project submission with comprehensive details"""
    st.header("📤 Project Submission")

    # Check if team is registered
    teams = data_manager.get_teams()
    team_names = [team["team_name"] for team in teams]

    if not team_names:
        st.warning("No teams registered yet. Please register your team first.")
        return

    with st.form("submit_project"):
        st.subheader("Project Details")
        team_name = st.selectbox("Select Your Team*", team_names)
        project_title = st.text_input("Project Title*")
        description = st.text_area("Project Description*", height=150)

        st.subheader("Problem Statement")
        problems = data_manager.get_problems()
        problem_options = ["Custom Problem"] + [f"{p['title']} ({p.get('category', 'General')})" for p in problems]
        selected_problem = st.selectbox("Problem Statement", problem_options)

        st.subheader("Technical Details")
        tech_stack = st.multiselect(
            "Technology Stack Used",
            ["Python", "JavaScript", "React", "Node.js", "Django", "Flask", "TensorFlow",
             "PyTorch", "MongoDB", "PostgreSQL", "Firebase", "AWS", "Docker", "Other"]
        )

        st.subheader("Project Links")
        github_link = st.text_input("GitHub Repository Link")
        demo_link = st.text_input("Live Demo/Video Link")

        if st.form_submit_button("Submit Project"):
            if not project_title or not description:
                st.error("Please fill in all required fields marked with *")
            else:
                try:
                    problem_id = ""
                    if selected_problem != "Custom Problem":
                        # Extract problem ID from selection
                        problem_index = problem_options.index(selected_problem) - 1
                        if 0 <= problem_index < len(problems):
                            problem_id = problems[problem_index].get("id", "")

                    submission_id = data_manager.submit_project(
                        team_name=team_name,
                        project_title=project_title,
                        description=description,
                        github_link=github_link,
                        demo_link=demo_link,
                        tech_stack=tech_stack,
                        problem_id=problem_id
                    )

                    st.success(f"✅ Project submitted successfully! Submission ID: {submission_id}")

                    # Show AI analysis using JudgingBot
                    if st.checkbox("Get AI Feedback on Your Submission"):
                        agents = initialize_agents()
                        project_data = {
                            "team_name": team_name,
                            "title": project_title,
                            "description": description,
                            "tech_stack": tech_stack,
                            "github_link": github_link,
                            "demo_link": demo_link
                        }

                        with st.spinner("Analyzing your project..."):
                            evaluation = agents["judging"].evaluate_project(project_data)
                            st.info(f"🤖 AI Analysis:\n{evaluation['ai_analysis']}")

                except ValueError as e:
                    st.error(f"Submission failed: {str(e)}")


def ai_mentor_chat():
    """AI Mentor Chat Interface"""
    st.header("🤖 AI Mentor - Get Coding Help")

    if not config_validation["groq_api_key"]:
        st.error("Groq API key not configured. Please add your API key to the .env file.")
        return

    agents = initialize_agents()
    mentor = agents["mentor"]

    # Chat interface
    if "mentor_messages" not in st.session_state:
        st.session_state.mentor_messages = []

    # Display chat history
    for message in st.session_state.mentor_messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Chat input
    if prompt := st.chat_input("Ask your coding question..."):
        # Add user message
        st.session_state.mentor_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        # Get AI response
        with st.chat_message("assistant"):
            with st.spinner("MentorBot is thinking..."):
                response = mentor.get_coding_help(prompt)
                st.write(response)
                st.session_state.mentor_messages.append({"role": "assistant", "content": response})

    # Quick help buttons
    st.subheader("Quick Help Topics")
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🐍 Python Help"):
            quick_response = mentor.get_coding_help("I need help with Python programming for my hackathon project")
            st.info(quick_response)

    with col2:
        if st.button("🌐 Web Development"):
            quick_response = mentor.get_coding_help("I need guidance on web development technologies")
            st.info(quick_response)

    with col3:
        if st.button("🧠 AI/ML Guidance"):
            quick_response = mentor.get_coding_help("I need help implementing AI/ML in my project")
            st.info(quick_response)

def challenge_generator_page():
    """AI-powered challenge generator"""
    st.header("🎯 AI Challenge Generator")

    if not config_validation["groq_api_key"]:
        st.error("Groq API key not configured. Please add your API key to the .env file.")
        return

    agents = initialize_agents()
    generator = agents["challenge_generator"]

    st.write("Generate new hackathon challenges using AI!")

    col1, col2 = st.columns(2)
    with col1:
        theme = st.text_input("Challenge Theme", value=Config.HACKATHON_THEME)
        category = st.selectbox("Category", COMPETITION_CATEGORIES)

    with col2:
        count = st.number_input("Number of Challenges", min_value=1, max_value=5, value=3)
        difficulty = st.selectbox("Difficulty Level", ["Easy", "Medium", "Hard", "Mixed"])

    if st.button("🚀 Generate Challenges"):
        with st.spinner("Generating challenges..."):
            challenges = generator.generate_challenges(theme, category, count)

            st.success(f"Generated {len(challenges)} challenges!")

            for i, challenge in enumerate(challenges, 1):
                with st.expander(f"Challenge {i}: {challenge.get('title', 'Generated Challenge')}"):
                    st.write(challenge.get('description', 'No description available'))

                    if st.button(f"Add Challenge {i} to Problem Bank", key=f"add_challenge_{i}"):
                        # Add to problem bank
                        data_manager.add_problem(
                            title=challenge.get('title', f'Generated Challenge {i}'),
                            description=challenge.get('description', ''),
                            category=category,
                            difficulty=challenge.get('difficulty', 'Medium'),
                            tech_stack=challenge.get('tech_stack', [])
                        )
                        st.success(f"Challenge {i} added to problem bank!")

def judge_panel():
    """Enhanced judge panel with AI assistance"""
    st.title("⚖️ Judge Panel")

    # Authentication
    password = st.text_input("Enter Judge Password", type="password")
    if password != Config.AUTHOR_PASSWORD:
        st.warning("🔒 Access Denied")
        return

    st.success("✅ Access Granted")

    # Judge information
    judge_name = st.text_input("Judge Name", value="Judge")

    # Get teams and projects
    teams = data_manager.get_teams()
    projects = {p["team_name"]: p for p in data_manager.get_projects()}

    if not teams:
        st.info("No teams registered yet.")
        return

    # Judging interface
    st.header("📊 Team Evaluation")

    # Team selection
    team_names = [team["team_name"] for team in teams]
    selected_team = st.selectbox("Select Team to Judge", team_names)

    if selected_team:
        team_data = next(team for team in teams if team["team_name"] == selected_team)
        project_data = projects.get(selected_team)

        # Display team information
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("👥 Team Information")
            st.write(f"**Team:** {team_data['team_name']}")
            st.write(f"**Members:** {', '.join(team_data.get('members', []))}")
            st.write(f"**College:** {team_data.get('college', 'Not specified')}")
            st.write(f"**Email:** {team_data.get('email', 'Not specified')}")

        with col2:
            st.subheader("📤 Project Submission")
            if project_data:
                st.write(f"**Title:** {project_data.get('project_title', 'Not provided')}")
                st.write(f"**Description:** {project_data.get('description', 'Not provided')}")
                st.write(f"**Tech Stack:** {', '.join(project_data.get('tech_stack', []))}")

                if project_data.get('github_link'):
                    st.markdown(f"**GitHub:** [View Repository]({project_data['github_link']})")
                if project_data.get('demo_link'):
                    st.markdown(f"**Demo:** [View Demo]({project_data['demo_link']})")
            else:
                st.warning("No project submitted yet")

        # AI Analysis
        if project_data and config_validation["groq_api_key"]:
            if st.button("🤖 Get AI Analysis"):
                agents = initialize_agents()
                judging_bot = agents["judging"]

                with st.spinner("Analyzing project..."):
                    evaluation = judging_bot.evaluate_project(project_data)
                    st.info(f"**AI Analysis:**\n{evaluation['ai_analysis']}")

        # Scoring form
        st.subheader("📝 Score Submission")
        with st.form(f"score_{selected_team}"):
            st.write("Rate each criteria from 1-10:")

            scores = {}
            for criteria in Config.JUDGING_CRITERIA:
                scores[criteria] = st.slider(
                    criteria.replace('_', ' ').title(),
                    1, Config.MAX_SCORE_PER_CRITERIA,
                    value=5,
                    key=f"{criteria}_{selected_team}"
                )

            comments = st.text_area("Additional Comments", height=100)

            if st.form_submit_button("Submit Score"):
                try:
                    score_id = data_manager.submit_score(
                        team_name=selected_team,
                        judge_name=judge_name,
                        scores=scores,
                        comments=comments
                    )
                    st.success(f"✅ Score submitted successfully! Score ID: {score_id}")
                except Exception as e:
                    st.error(f"Failed to submit score: {str(e)}")

        # Show existing scores for this team
        team_scores = data_manager.get_team_scores(selected_team)
        if team_scores:
            st.subheader("📈 Previous Scores")
            for score in team_scores:
                with st.expander(f"Score by {score['judge_name']} - Total: {score['total_score']}"):
                    for criteria, value in score['scores'].items():
                        st.write(f"**{criteria.replace('_', ' ').title()}:** {value}")
                    if score.get('comments'):
                        st.write(f"**Comments:** {score['comments']}")

def leaderboard():
    """Real-time leaderboard with analytics"""
    st.header("🏆 Live Leaderboard")

    leaderboard_data = data_manager.get_leaderboard()

    if not leaderboard_data:
        st.info("No teams scored yet.")
        return

    # Display leaderboard
    st.subheader("🥇 Current Rankings")

    for entry in leaderboard_data:
        if entry["total_average"] > 0:  # Only show teams with scores
            col1, col2, col3, col4 = st.columns([1, 3, 2, 2])

            with col1:
                # Rank with medal emoji
                rank = entry["rank"]
                if rank == 1:
                    st.markdown("🥇 **1st**")
                elif rank == 2:
                    st.markdown("🥈 **2nd**")
                elif rank == 3:
                    st.markdown("🥉 **3rd**")
                else:
                    st.markdown(f"**{rank}th**")

            with col2:
                st.write(f"**{entry['team_name']}**")
                st.write(f"*{entry['college']}*")

            with col3:
                st.metric("Total Score", f"{entry['total_average']:.1f}")
                st.write(f"Judges: {entry['judge_count']}")

            with col4:
                if entry["has_submission"]:
                    st.write(f"✅ {entry['project_title']}")
                else:
                    st.write("❌ No submission")

    # Analytics
    st.subheader("📊 Competition Analytics")

    # Create charts
    if leaderboard_data:
        # Score distribution
        scores_df = pd.DataFrame([
            {"Team": entry["team_name"], "Score": entry["total_average"]}
            for entry in leaderboard_data if entry["total_average"] > 0
        ])

        if not scores_df.empty:
            fig = px.bar(scores_df, x="Team", y="Score", title="Team Scores")
            fig.update_layout(xaxis_tickangle=45)
            st.plotly_chart(fig, width="stretch")

        # Statistics
        stats = data_manager.get_statistics()
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Total Teams", stats["total_teams"])
        with col2:
            st.metric("Submissions", f"{stats['total_submissions']}")
        with col3:
            st.metric("Submission Rate", f"{stats['submission_rate']:.1f}%")
        with col4:
            st.metric("Colleges", stats["total_colleges"])


def admin_panel():
    """Admin panel for event management"""
    st.header("🔧 Admin Panel")

    password = st.text_input("Enter Admin Password", type="password")
    if password != Config.AUTHOR_PASSWORD:
        st.warning("🔒 Access Denied")
        return

    st.success("✅ Admin Access Granted")

    tab1, tab2, tab3, tab4 = st.tabs(["📊 Statistics", "📝 Manage Problems", "📧 Outreach", "⚙️ Settings"])

    with tab1:
        st.subheader("Event Statistics")
        stats = data_manager.get_statistics()

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Teams", stats["total_teams"])
            st.metric("Total Submissions", stats["total_submissions"])
        with col2:
            st.metric("Colleges Reached", stats["total_colleges"])
            st.metric("Submission Rate", f"{stats['submission_rate']:.1f}%")
        with col3:
            st.metric("Scored Teams", stats["scored_teams"])
            st.metric("Total Scores", stats["total_scores"])

        # Display college list
        if stats["colleges_list"]:
            st.subheader("Participating Colleges")
            for college in stats["colleges_list"]:
                if college != "Unknown":
                    st.write(f"• {college}")

    with tab2:
        st.subheader("Manage Problem Statements")

        # Add new problem
        with st.form("add_problem"):
            st.write("**Add New Problem Statement**")
            title = st.text_input("Title")
            description = st.text_area("Description")
            category = st.selectbox("Category", COMPETITION_CATEGORIES)
            difficulty = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"])
            tech_stack = st.multiselect("Suggested Tech Stack",
                ["Python", "JavaScript", "React", "Node.js", "Django", "Flask",
                 "TensorFlow", "PyTorch", "MongoDB", "PostgreSQL", "Other"])

            if st.form_submit_button("Add Problem"):
                if title and description:
                    problem_id = data_manager.add_problem(title, description, category, difficulty, tech_stack)
                    st.success(f"Problem added successfully! ID: {problem_id}")
                else:
                    st.error("Please fill in title and description")

        # Display existing problems
        st.subheader("Existing Problems")
        problems = data_manager.get_problems()
        for problem in problems:
            with st.expander(f"{problem['title']} ({problem.get('category', 'General')})"):
                st.write(problem['description'])
                st.write(f"**Difficulty:** {problem.get('difficulty', 'Medium')}")
                if problem.get('tech_stack'):
                    st.write(f"**Tech Stack:** {', '.join(problem['tech_stack'])}")

    with tab3:
        st.subheader("Outreach Management")

        # Add outreach contact
        with st.form("add_outreach"):
            st.write("**Add Outreach Contact**")
            college_name = st.text_input("College/University Name")
            contact_person = st.text_input("Contact Person")
            contact_email = st.text_input("Contact Email")
            contact_phone = st.text_input("Contact Phone")
            outreach_method = st.selectbox("Outreach Method",
                ["Email", "WhatsApp", "Instagram", "Discord", "Direct Contact", "Other"])

            if st.form_submit_button("Add Contact"):
                if college_name and contact_person and contact_email:
                    contact_id = data_manager.add_outreach_contact(
                        college_name, contact_person, contact_email,
                        contact_phone, outreach_method
                    )
                    st.success(f"Contact added successfully! ID: {contact_id}")
                else:
                    st.error("Please fill in required fields")

        # Display outreach data
        outreach_data = data_manager.get_outreach_data()
        if outreach_data:
            st.subheader("Outreach Contacts")
            for contact in outreach_data:
                with st.expander(f"{contact['college_name']} - {contact['contact_person']}"):
                    st.write(f"**Email:** {contact['contact_email']}")
                    st.write(f"**Phone:** {contact.get('contact_phone', 'Not provided')}")
                    st.write(f"**Method:** {contact.get('outreach_method', 'Not specified')}")
                    st.write(f"**Status:** {contact.get('status', 'contacted')}")

                    # Update status
                    new_status = st.selectbox(
                        "Update Status",
                        ["contacted", "responded", "interested", "registered", "declined"],
                        index=["contacted", "responded", "interested", "registered", "declined"].index(contact.get('status', 'contacted')),
                        key=f"status_{contact['id']}"
                    )
                    response_note = st.text_input("Response Note", key=f"note_{contact['id']}")

                    if st.button("Update", key=f"update_{contact['id']}"):
                        data_manager.update_outreach_status(contact['id'], new_status, response_note)
                        st.success("Status updated!")
                        st.experimental_rerun()

    with tab4:
        st.subheader("System Settings")
        st.write("**Current Configuration:**")
        st.write(f"• Hackathon Name: {Config.HACKATHON_NAME}")
        st.write(f"• Theme: {Config.HACKATHON_THEME}")
        st.write(f"• Event Date: {Config.EVENT_DATE}")
        st.write(f"• Registration Deadline: {Config.REGISTRATION_DEADLINE}")

        st.subheader("System Status")
        for key, status in config_validation.items():
            status_icon = "✅" if status else "❌"
            st.write(f"{status_icon} {key.replace('_', ' ').title()}")

# Main Application
def main():
    """Main application with navigation"""

    # Sidebar navigation
    display_system_status()

    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🧭 Navigation")

    pages = {
        "🏠 Home": home_page,
        "👥 Team Registration": team_registration,
        "📤 Project Submission": project_submission,
        "🤖 AI Mentor": ai_mentor_chat,
        "🎯 Challenge Generator": challenge_generator_page,
        "🏆 Leaderboard": leaderboard,
        "⚖️ Judge Panel": judge_panel,
        "🔧 Admin Panel": admin_panel
    }

    selected_page = st.sidebar.radio("Select Page", list(pages.keys()))

    # Display selected page
    pages[selected_page]()

    # Footer
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📞 Support")
    st.sidebar.markdown("Need help? Contact the organizers!")

    # Quick stats in sidebar
    stats = data_manager.get_statistics()
    st.sidebar.markdown("### 📊 Quick Stats")
    st.sidebar.metric("Teams", stats["total_teams"])
    st.sidebar.metric("Submissions", stats["total_submissions"])

if __name__ == "__main__":
    main()
    
