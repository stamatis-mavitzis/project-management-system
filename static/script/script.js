// ===========================
// Admin Manage Users Actions
// ===========================

// --- Activate User ---
function activateUser(username) {
  if (!confirm(`Activate user ${username}?`)) return;
  fetch(`/activate_user/${username}`, { method: "POST" })
    .then(res => res.json())
    .then(data => {
      if (data.message) {
        alert(data.message);
        location.reload();
      } else {
        alert(`❌ Error activating ${username}: ${data.error}`);
      }
    })
    .catch(err => alert(`⚠️ Network error: ${err}`));
}

// --- Deactivate User ---
function deactivateUser(username) {
  if (!confirm(`Deactivate user ${username}?`)) return;
  fetch(`/deactivate_user/${username}`, { method: "POST" })
    .then(res => res.json())
    .then(data => {
      if (data.message) {
        alert(data.message);
        location.reload();
      } else {
        alert(`❌ Error deactivating ${username}: ${data.error}`);
      }
    })
    .catch(err => alert(`⚠️ Network error: ${err}`));
}

// --- Change User Role ---
function changeRole(username) {
  const newRole = prompt("Enter new role (ADMIN / TEAM_LEADER / MEMBER):");
  if (!newRole) return;

  fetch(`/change_role/${username}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ role: newRole })
  })
    .then(res => res.json())
    .then(data => {
      if (data.message) {
        alert(data.message);
        location.reload();
      } else {
        alert(`❌ Failed to change role for ${username}: ${data.error}`);
      }
    })
    .catch(err => alert(`⚠️ Network error: ${err}`));
}

// --- View Team ---
function viewTeam(teamId) {
  window.location.href = `/admin-viewTeam/${teamId}`;
}

// --- Delete Team ---
function deleteTeam(teamId) {
  if (!confirm("Are you sure you want to delete this team?")) return;
  fetch(`/admin-deleteTeam/${teamId}`, { method: "POST" })
    .then(res => res.json())
    .then(data => {
      if (data.message) {
        alert(data.message);
        location.reload();
      } else {
        alert(`❌ Error deleting team: ${data.error}`);
      }
    })
    .catch(err => alert(`⚠️ Network error: ${err}`));
}


// ===========================
// Redirect Buttons (UI Navigation)
// ===========================
document.addEventListener("DOMContentLoaded", function() {
    // redirect to main pages
    const redirectButton_home = document.getElementById("redirect_to_home");
    const redirectButton_admin_or_teamLeader_or_member = document.getElementById("redirectButton_admin_or_teamLeader_or_member");
    const redirectButton_logout = document.getElementById("redirectButton_logout");
    
    // redirect to options
    const redirectButton_admin_options = document.getElementById("redirectButton_admin_options");
    const redirectButton_teamLeader_options = document.getElementById("redirectButton_teamLeader_options");
    const redirectButton_member_options = document.getElementById("redirectButton_member_options");

    // redirect to login / signup
    const redirectButton_admin_login = document.getElementById("redirectButton_admin_login");
    const redirectButton_admin_signup = document.getElementById("redirectButton_admin_signup");
    const redirectButton_teamLeader_login = document.getElementById("redirectButton_teamLeader_login");
    const redirectButton_teamLeader_signup = document.getElementById("redirectButton_teamLeader_signup");
    const redirectButton_member_login = document.getElementById("redirectButton_member_login");
    const redirectButton_member_signup = document.getElementById("redirectButton_member_signup");

    // main pages
    const redirectButton_admin_mainpage = document.getElementById("redirectButton_admin_mainpage");
    const redirectButton_teamLeader_mainpage = document.getElementById("redirectButton_teamLeader_mainpage");
    const redirectButton_member_mainpage  = document.getElementById("redirectButton_member_mainpage");

    // member mainpage
    const member_redirect_teams_included = document.getElementById("member_redirect_teams_included");
    const member_redirect_projects = document.getElementById("member_redirect_projects");
    const member_redirect_tasks = document.getElementById("member_redirect_tasks");
    const member_redirect_notifications_and_deadlines = document.getElementById("member_redirect_notifications_and_deadlines");

    // admin mainpage
    const admin_redirect_manageUsers = document.getElementById("admin_redirect_manageUsers");
    const admin_redirect_manageTeams = document.getElementById("admin_redirect_manageTeams");
    const admin_redirect_show_tasks_and_projects = document.getElementById("admin_redirect_show_tasks_and_projects");


    // team leader
    const teamLeader_redirect_manageTeams = document.getElementById("teamLeader_redirect_manageTeams");
    const teamLeader_redirect_manageTasksProjects = document.getElementById("teamLeader_redirect_manageTasksProjects");


    // --- Home ---
    if (redirectButton_home) {
       redirectButton_home.addEventListener("click", () => window.location.href = "/");
    }
    if (redirectButton_admin_or_teamLeader_or_member) {
        redirectButton_admin_or_teamLeader_or_member.addEventListener("click", () => window.location.href = "/admin-or-teamLeader-or-member");
    }
    if (redirectButton_logout) {
        redirectButton_logout.addEventListener("click", () => window.location.href = "/logout");
    }

    // --- Options ---
    if (redirectButton_admin_options) {
        redirectButton_admin_options.addEventListener("click", () => window.location.href = "/admin-options");
    }
    if (redirectButton_teamLeader_options) {
        redirectButton_teamLeader_options.addEventListener("click", () => window.location.href = "/teamLeader-options");
    }
    if (redirectButton_member_options) {
        redirectButton_member_options.addEventListener("click", () => window.location.href = "/member-options");
    }

    // --- Login & Signups ---
    if (redirectButton_admin_login) redirectButton_admin_login.addEventListener("click", () => window.location.href = "/admin-login");
    if (redirectButton_admin_signup) redirectButton_admin_signup.addEventListener("click", () => window.location.href = "/admin-signup");
    if (redirectButton_teamLeader_login) redirectButton_teamLeader_login.addEventListener("click", () => window.location.href = "/teamLeader-login");
    if (redirectButton_teamLeader_signup) redirectButton_teamLeader_signup.addEventListener("click", () => window.location.href = "/teamLeader-signup");
    if (redirectButton_member_login) redirectButton_member_login.addEventListener("click", () => window.location.href = "/member-login");
    if (redirectButton_member_signup) redirectButton_member_signup.addEventListener("click", () => window.location.href = "/member-signup");

    // --- Main Pages ---
    if (redirectButton_admin_mainpage) redirectButton_admin_mainpage.addEventListener("click", () => window.location.href = "/admin-mainpage");
    if (redirectButton_teamLeader_mainpage) redirectButton_teamLeader_mainpage.addEventListener("click", () => window.location.href = "/teamLeader-mainpage");
    if (redirectButton_member_mainpage) redirectButton_member_mainpage.addEventListener("click", () => window.location.href = "/member-mainpage");

    // --- Member Main Page ---
    if (member_redirect_teams_included) member_redirect_teams_included.addEventListener("click", () => window.location.href = "/member-teamsIncluded");
    if (member_redirect_projects) member_redirect_projects.addEventListener("click", () => window.location.href = "/member-projects");
    if (member_redirect_tasks) member_redirect_tasks.addEventListener("click", () => window.location.href = "/member-tasks");
    if (member_redirect_notifications_and_deadlines) member_redirect_notifications_and_deadlines.addEventListener("click", () => window.location.href = "/member-notifications_and_deadlines");

    // --- Admin Main Page ---
    if (admin_redirect_manageUsers) admin_redirect_manageUsers.addEventListener("click", () => window.location.href = "/admin-manageUsers");
    if (admin_redirect_manageTeams) admin_redirect_manageTeams.addEventListener("click", () => window.location.href = "/admin-manageTeams");
    if (admin_redirect_show_tasks_and_projects) admin_redirect_show_tasks_and_projects.addEventListener("click", () => window.location.href = "/admin-show_tasks_and_projects");

    // --- Team Leader Main Page ---
    if (teamLeader_redirect_manageTeams) teamLeader_redirect_manageTeams.addEventListener("click", () => window.location.href = "/teamLeader-manageTeams");
    if (teamLeader_redirect_manageTasksProjects) teamLeader_redirect_manageTasksProjects.addEventListener("click", () => window.location.href = "/teamLeader-manageTasksProjects");
});
