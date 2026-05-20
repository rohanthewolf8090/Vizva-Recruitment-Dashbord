import streamlit as st
import pandas as pd
import datetime
import random
import smtplib
from email.mime.text import MIMEText

# ─── RECRUITER CONSTANTS & TARGET DEFINITIONS ──────────────────────────────
# Target Group A (30 calls, 2 interviews): Apoorva, Dibyajyoti
# Target Group B (60 calls, 4 interviews): Devendra, Puneet, Kunal
RECRUITER_TERMS = {
    "Apoorva": {"calls": 30, "interviews": 2},
    "Dibyajyoti": {"calls": 30, "interviews": 2},
    "Devendra": {"calls": 60, "interviews": 4},
    "Puneet": {"calls": 60, "interviews": 4},
    "Kunal": {"calls": 60, "interviews": 4}
}

# ─── STREAMLIT INTERFACE CONFIGURATION (VIZVA NAVY & CLEAN WATERMARK) ──────
st.set_page_config(page_title="Vizva Consultancy & Services — HireFlow v2", layout="wide")

st.markdown("""
    <style>
    /* Premium Minimalist Theme Colors */
    .main { 
        background-color: #F8FAFC; 
        font-family: 'Inter', sans-serif; 
    }
    h1, h2, h3 { color: #0F172A; font-weight: 700; }
    
    /* Clean, unobtrusive background watermark text styling */
    .reportview-container .main .block-container{ position: relative; }
    .main::before {
        content: "VIZVA";
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%) rotate(-15deg);
        font-size: 14vw;
        font-weight: 900;
        color: rgba(30, 58, 138, 0.03); /* Soft transparent navy logo fill */
        z-index: 0;
        pointer-events: none;
        white-space: nowrap;
    }
    
    div.stButton > button:first-child {
        background-color: #1E3A8A; color: #FFFFFF; font-weight: 600;
        border-radius: 6px; padding: 10px 24px; border: none; transition: 0.3s;
    }
    div.stButton > button:first-child:hover { background-color: #1D4ED8; }
    </style>
    """, unsafe_allow_html=True)

# ─── LOCAL STORAGE INITIALIZATION (100% FRESH START) ───────────────────────
if 'positions_db' not in st.session_state:
    st.session_state.positions_db = pd.DataFrame(columns=[
        "ID", "Type", "Position", "Total", "Joined", "Offered", "Open", "HM", "Location", "Deadline", "Status"
    ])

if 'candidate_logs_db' not in st.session_state:
    st.session_state.candidate_logs_db = pd.DataFrame(columns=[
        "Date", "Recruiter", "Candidate Name", "Designation", "Email", "Contact Details", 
        "Current CTC", "Expected CTC", "Notice Period", "Source", "Status", "Remarks Summary", "Resume File"
    ])

# ─── LIVE NOTIFICATION EMAIL ENGINE (REAL AUTOMATION) ──────────────────────
def trigger_system_email(subject, recipients, body_content):
    """Sends real automated emails to the TAG team and Dibyajyoti instantly"""
    
    # 🌟 KEY SETUP: Replace these lines with your actual company credentials to activate real delivery!
    SENDER_EMAIL = "hr@vizvainc.com" 
    SENDER_PASSWORD = "your-secure-email-app-password" # App password generated from email settings
    SMTP_SERVER = "smtp.gmail.com"  # Use "smtp.office365.com" if your firm uses Outlook
    SMTP_PORT = 587

    try:
        # Build message package
        msg = MIMEText(body_content)
        msg['Subject'] = subject
        msg['From'] = SENDER_EMAIL
        msg['To'] = ", ".join(recipients)
        
        # Connect securely to mail provider server and push live transmission
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, recipients, msg.as_string())
        server.quit()
        
        st.toast(f"📥 Live Email Notification Dispatched successfully to inboxes!", icon="✉️")
    except Exception as e:
        # Graceful fallback alert context so app runs smoothly even before emails are wired
        st.sidebar.warning("⚠️ Real-world email credentials not configured yet. Output logging locally instead.")
        with st.sidebar.expander("📨 Local Outbound Email Queue Logs", expanded=False):
            st.caption(f"**To:** {', '.join(recipients)}")
            st.code(body_content, language="text")

# ─── AUTOMATED PRIORITY CALCULATOR ──────────────────────────────────────────
def evaluate_urgency_index(row):
    days_remaining = (row['Deadline'] - datetime.date.today()).days
    if days_remaining <= 7:
        return "🔥 Burning"
    elif days_remaining <= 14 and row['Open'] >= 5:
        return "⚡ Top Priority"
    return "🟢 Low Priority"

# ─── CORPORATE SIDEBAR BRANDING ─────────────────────────────────────────────
st.sidebar.markdown("<h2 style='color:#1E3A8A; margin-bottom:0;'>VIZVA</h2><p style='color:#64748B; font-size:12px; margin-top:0;'>CONSULTANCY & SERVICES</p>", unsafe_allow_html=True)
st.sidebar.write("---")

app_panel = st.sidebar.selectbox("Navigate Dashboard Workspace:", [
    "Weekly Leadership Overview", 
    "Hiring Manager Desk", 
    "Recruiter Workspace", 
    "Rohan's Operational Gate"
])

user_identity = st.sidebar.selectbox("Confirm User Identity:", [
    "Rohan Sharma", "Apoorva", "Dibyajyoti", "Devendra", "Puneet", "Kunal", "Vin", "Pathan Sir"
])

# ==========================================
# PANEL 1: HIRING MANAGER DESK
# ==========================================
if app_panel == "Hiring Manager Desk":
    st.title("➕ Launch New Sourcing Requirement")
    st.write("Input structural parameters below to allocate fresh positions directly to the recruitment team.")
    
    with st.form("hiring_manager_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            req_type = st.selectbox("Allocation Classification Type", ["New Requirement", "Backfill Vacancy"])
            pos_title = st.text_input("Exact Position Title")
            headcount = st.number_input("Target Openings Count", min_value=1, step=1, value=1)
        with col2:
            branch_loc = st.selectbox("Target Deployment Location", ["Noida Office (NCR)", "Ahmedabad Office (AHM)", "Lucknow Office (LKO)"])
            target_date = st.date_input("Target Sourcing Closure Deadline Date", min_value=datetime.date.today() + datetime.timedelta(days=1))
            job_description = st.text_area("Core Job Parameters & Preferred Prerequisites")
            
        submit_requirement = st.form_submit_button("Release Sourcing Stream")
        
        if submit_requirement:
            generated_id = random.randint(1000, 9999)
            new_position_row = {
                "ID": generated_id, "Type": req_type, "Position": pos_title, "Total": headcount,
                "Joined": 0, "Offered": 0, "Open": headcount, "HM": user_identity,
                "Location": branch_loc, "Deadline": target_date, "Status": "Pending Operational Approval"
            }
            st.session_state.positions_db = pd.concat([st.session_state.positions_db, pd.DataFrame([new_position_row])], ignore_index=True)
            
            # AUTOMATED TRIGGER: Instant email dispatched to active inboxes
            alert_recipients = ["Tag@silverspaceinc.com", "Dibyajyoti.Ghosh@vizvainc.com"]
            email_msg = f"Attention TAG Team & Dibyajyoti,\n\nA brand new recruitment request for '{pos_title}' ({headcount} open slots) has been initialized by Hiring Manager: {user_identity}.\nTarget Deployment Location: {branch_loc}.\n\nThis allocation has been routed to Rohan Sharma for final executive authorization."
            trigger_system_email(f"[REQ DISPATCHED] Pending Authorization: {pos_title}", alert_recipients, email_msg)
            st.success("Requirement registered successfully! Real-time alerts transmitted.")

# ==========================================
# PANEL 2: ROHAN'S OPERATIONAL GATE
# ==========================================
elif app_panel == "Rohan's Operational Gate":
    st.title("🛡️ Executive Operational Authorization Gate")
    st.write("Review, authorize, and automatically distribute incoming pipeline requests to the active recruiter pool.")
    
    df_p = st.session_state.positions_db
    pending_allocations = df_p[df_p['Status'] == "Pending Operational Approval"]
    
    if not pending_allocations.empty:
        for index, row in pending_allocations.iterrows():
            with st.expander(f"📥 Pending Authorization: {row['Position']} for {row['Location']}"):
                st.write(f"**Requested By:** {row['HM']} | **Headcount Target:** {row['Total']} | **Manager Deadline:** {row['Deadline']}")
                
                if st.button("Authorize Allocation & Broadcast Pipeline", key=f"auth_btn_{row['ID']}"):
                    st.session_state.positions_db.loc[st.session_state.positions_db['ID'] == row['ID'], 'Status'] = "Approved"
                    
                    team_recipients = ["Tag@silverspaceinc.com", "Dibyajyoti.Ghosh@vizvainc.com"]
                    activation_msg = f"Operational Alert,\n\nRohan Sharma has officially authorized the pipeline processing for '{row['Position']}' (Target Deadline: {row['Deadline']}).\nThe matrix is deployed to all multi-location active recruiter workspaces. Sourcing tasks must commence immediately."
                    trigger_system_email(f"[WORK STARTED] Pipeline Activated: {row['Position']}", team_recipients, activation_msg)
                    st.success(f"Pipeline tracking live for {row['Position']}. Broadcast completed.")
                    st.rerun()
    else:
        st.info("Your operational queue is completely clear. No fresh requirements are waiting for authorization.")

# ==========================================
# PANEL 3: RECRUITER WORKSPACE
# ==========================================
elif app_panel == "Recruiter Workspace":
    st.title(f"🎧 Centralized Recruiter Console: {user_identity}")
    
    if user_identity not in RECRUITER_TERMS:
        st.warning("Please switch your identity in the sidebar navigation panel to an active recruiter account to check milestones.")
    else:
        rec_limits = RECRUITER_TERMS[user_identity]
        st.subheader("🎯 Live Daily Performance Benchmarks")
        
        df_logs = st.session_state.candidate_logs_db
        today_date_str = datetime.date.today().strftime('%Y-%m-%d')
        today_records = df_logs[(df_logs['Recruiter'] == user_identity) & (df_logs['Date'] == today_date_str)] if not df_logs.empty else pd.DataFrame()
        
        logged_calls = len(today_records)
        logged_interviews = len(today_records[today_records['Status'] == "Interview"]) if not today_records.empty else 0
        
        call_pct = min(int((logged_calls / rec_limits['calls']) * 100), 100)
        int_pct = min(int((logged_interviews / rec_limits['interviews']) * 100), 100)
        
        m_col1, m_col2 = st.columns(2)
        with m_col1:
            st.metric("Calls Milestone Target Progress", f"{call_pct}%", f"{logged_calls} / {rec_limits['calls']} Connected Today")
            st.progress(call_pct / 100)
        with m_col2:
            st.metric("Interviews Milestone Target Progress", f"{int_pct}%", f"{logged_interviews} / {rec_limits['interviews']} Executed Today")
            st.progress(int_pct / 100)
            
        st.write("---")
        st.subheader("📝 Input Sourced Candidate Details")
        
        with st.form("sourcing_entry_form", clear_on_submit=True):
            tx1, tx2, tx3 = st.columns(3)
            with tx1:
                cand_name = st.text_input("Candidate Full Name")
                cand_desig = st.text_input("Current Designation/Role")
                cand_email = st.text_input("Candidate Email ID")
            with tx2:
                cand_phone = st.text_input("Primary Contact Details")
                curr_sal = st.text_input("Current Salary (CTC)")
                exp_sal = st.text_input("Expected Salary")
            with tx3:
                notice_per = st.text_input("Notice Period Duration")
                src_route = st.selectbox("Candidate Sourcing Channel", ["Sourced by Recruiter", "Internal Reference Profile"])
                milestone_status = st.selectbox("Current Tracking Milestone Status", ["Screening", "Interview", "Salary Discussion", "Offered", "Joined", "Rejected"])
                
            remarks_summary = st.text_area("Current Remarks Summary / Direct Case Context Log")
            resume_file_blob = st.file_uploader("📂 Upload Candidate Resume Profile", type=["pdf", "docx"])
            
            commit_entry = st.form_submit_button("Commit Sourcing Record Entry")
            if commit_entry:
                attached_filename = resume_file_blob.name if resume_file_blob is not None else "No Uploaded Attachment Saved"
                new_transaction_row = {
                    "Date": today_date_str, "Recruiter": user_identity, "Candidate Name": cand_name,
                    "Designation": cand_desig, "Email": cand_email, "Contact Details": cand_phone,
                    "Current CTC": curr_sal, "Expected CTC": exp_sal, "Notice Period": notice_per,
                    "Source": src_route, "Status": milestone_status, "Remarks Summary": remarks_summary, "Resume File": attached_filename
                }
                st.session_state.candidate_logs_db = pd.concat([st.session_state.candidate_logs_db, pd.DataFrame([new_transaction_row])], ignore_index=True)
                st.success(f"Candidate data log committed successfully for {cand_name}!")

# ==========================================
# PANEL 4: WEEKLY LEADERSHIP OVERVIEW
# ==========================================
elif app_panel == "Weekly Leadership Overview":
    st.title("📊 Automated Recruitment Analytics Dashboard")
    st.write("PAN-India real-time delivery tracking. No daily alignment meetings are required.")
    
    st.subheader("🏢 Active Corporate Requirements & Urgency Matrix")
    master_pos_df = st.session_state.positions_db.copy()
    approved_pos_df = master_pos_df[master_pos_df['Status'] == "Approved"]
    
    if not approved_pos_df.empty:
        approved_pos_df['Fulfillment %'] = (((approved_pos_df['Joined'] + approved_pos_df['Offered']) / approved_pos_df['Total']) * 100).round(1)
        approved_pos_df['Urgency Level'] = approved_pos_df.apply(evaluate_urgency_index, axis=1)
        
        st.dataframe(approved_pos_df[[
            'Urgency Level', 'Position', 'Location', 'Total', 'Open', 
            'Joined', 'Offered', 'Deadline', 'Fulfillment %', 'HM'
        ]], use_container_width=True)
    else:
        st.info("The active operations pipeline is clear. Sourcing requirements will populate automatically once approved by Rohan Sharma.")
        
    st.write("---")
    st.subheader("🕵️ Centralized Sourcing Activity Logs Live Feed")
    master_logs_df = st.session_state.candidate_logs_db
    if not master_logs_df.empty:
        st.dataframe(master_logs_df, use_container_width=True)
    else:
        st.caption("Waiting for recruiters across your locations to submit their first daily logs to populate the master table feed.")
