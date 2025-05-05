import {
  getAuthToken,
  createTicket,
  fetchTickets,
  getAIRecommendation
} from "./api.js";



// Helper: Decode JWT payload
function decodeToken(token) {
  try {
    const payload = JSON.parse(atob(token.split(".")[1]));
    console.log("Logged in as:", payload.username || payload.email);
    return payload;
  } catch (e) {
    console.error("Failed to decode token", e);
    return null;
  }
}


// Helper: Redirect user
function redirectTo(path) {
  window.location.href = path;
}

const technicianNames = {
  1: "Trevone Graves",
  2: "Ethan Varisco",
  3: "Terry Fox",
  4: "Laelan Reyes",
  5: "Alyssa Montoya"
};

// Helper: Render tickets on ticket list page
async function renderTickets(limit = null) {
  const token = localStorage.getItem("authToken");
  const tableBody = document.getElementById("ticket-table");

  if (!tableBody) return;

  let tickets = await fetchTickets(token);

  // Ensure tickets is an array
  if (!Array.isArray(tickets)) {
    tickets = [];
  }

  // If a limit is provided, slice the tickets to the limit
  if (limit) {
    tickets = tickets.slice(0, limit);
  }

  if (!tickets.length) {
    tableBody.innerHTML = "<tr><td colspan='5'>No tickets found.</td></tr>";
    return;
  }

  tableBody.innerHTML = ""; 

  tickets.forEach(ticket => {
    // Use technician ID to get their full name, default to "Unassigned" if not found
    const technicianName = technicianNames[ticket.assigned_to] || "Unassigned";

    const row = document.createElement("tr");
    row.innerHTML = `
      <td>${ticket.id}</td>
      <td>${ticket.title}</td>
      <td>${ticket.status || "Open"}</td>
      <td>${ticket.priority}</td>
      <td>${technicianName}</td>
    `;
    row.style.cursor = "pointer";
    row.addEventListener("click", () => {
      redirectTo(`/pages/ticket-card.html?id=${ticket.id}`);
    });
    tableBody.appendChild(row);
  });
}


// Helper: Fetch individual ticket + AI Recommendation
async function renderTicketDetails() {
  const id = new URLSearchParams(window.location.search).get("id");
  if (!id) return;

  const token = localStorage.getItem("authToken");
  const tickets = await fetchTickets(token);
  const ticket = tickets.find(t => t.id.toString() === id);

  if (!ticket) {
    document.getElementById("ticket-detail").innerText = "Ticket not found.";
    return;
  }

  const technicianName = technicianNames[ticket.assigned_to] || "Unassigned";

  document.getElementById("ticket-id").innerText = ticket.id;
  document.getElementById("ticket-title").innerText = ticket.title;
  document.getElementById("ticket-description").innerText = ticket.description;
  document.getElementById("ticket-status").innerText = ticket.status;
  document.getElementById("ticket-priority").innerText = ticket.priority;
  document.getElementById("ticket-assigned").innerText = technicianName;

  const markInProgressButton = document.getElementById("mark-in-progress");
  const resolveButton = document.getElementById("resolve-ticket");

  if (ticket.status === "In Progress") {
    markInProgressButton.disabled = true; 
  } else if (ticket.status === "Resolved") {
    resolveButton.disabled = true; 
  }

  // Add event listeners to the buttons
  markInProgressButton.addEventListener("click", () => changeTicketStatus('In Progress'));
  resolveButton.addEventListener("click", () => changeTicketStatus('Resolved'));

  // Trigger AI Recommendation
  getAIRecommendation(ticket.description);
}

// Helper: Change ticket status
async function changeTicketStatus(newStatus) {
  const ticketId = new URLSearchParams(window.location.search).get("id");
  if (!ticketId) return;

  const token = localStorage.getItem("authToken");

  const response = await fetch(`http://127.0.0.1:8000/api/tickets/${ticketId}/`, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${token}`,
    },
    body: JSON.stringify({
      status: newStatus,
    }),
  });

  if (response.ok) {
    alert(`Ticket marked as ${newStatus}`);
    // After successfully updating the ticket status, refresh the ticket details
    await renderTicketDetails();
  } else {
    const errorData = await response.json();
    alert(`Failed to update status: ${errorData.detail}`);
  }
}


// Helper: Render ticket counts
async function renderTicketCounts() {
  const token = localStorage.getItem("authToken");

  // Fetch the tickets
  const tickets = await fetchTickets(token);

  // Log all statuses for debugging
  console.log("---- Ticket Status Debug ----");
  const uniqueStatuses = new Set();
  tickets.forEach(ticket => {
    console.log(`Ticket ID ${ticket.id} - Status: [${ticket.status}]`);
    uniqueStatuses.add(ticket.status);
  });
  console.log("Unique Status Values:", Array.from(uniqueStatuses));

  // Initialize counters
  let openCount = 0;
  let inProgressCount = 0;
  let resolvedCount = 0;

  // Count the tickets based on their status
  tickets.forEach(ticket => {
    const status = ticket.status.trim(); 

    if (status === "Open") {
      openCount++;
    } else if (status === "In Progress") {
      inProgressCount++;
    } else if (status === "Resolved") {
      resolvedCount++;
    }
  });

  // Update the status boxes with the count
  document.getElementById("open-count").innerText = openCount;
  document.getElementById("in-progress-count").innerText = inProgressCount;
  document.getElementById("resolved-count").innerText = resolvedCount;
}


// Initialize App Logic
document.addEventListener("DOMContentLoaded", async () => {
  const path = window.location.pathname;
  const token = localStorage.getItem("authToken");

  const isLoginPage = path.endsWith("/pages/login.html");
  const isSignupPage = path.endsWith("/pages/signup.html");
  const isIndexPage = path.endsWith("/index.html");
  const isCreateTicketPage = path.endsWith("/pages/create-ticket.html");
  const isTicketListPage = path.endsWith("/pages/ticket-list.html");
  const isTicketCardPage = path.endsWith("/pages/ticket-card.html");

  // Redirect rules
  if (!token && !isLoginPage && !isSignupPage) {
    return redirectTo("/pages/login.html");
  }
  if (token && (isLoginPage || isSignupPage)) {
    return redirectTo("/index.html");
  }

  // Show logout link
  const logoutLink = document.getElementById("logout-link");
  if (logoutLink && token) {
    logoutLink.style.display = "block";
    logoutLink.addEventListener("click", () => {
      localStorage.removeItem("authToken");
      redirectTo("/pages/login.html");
    });
  }

  // Decode token (just for logging/optional use)
  if (token) decodeToken(token);

  // === Page-specific Logic ===

  // LOGIN
  if (isLoginPage) {
    const loginForm = document.getElementById("login-form");
    loginForm?.addEventListener("submit", async e => {
      e.preventDefault();
      const username = e.target.username.value;
      const password = e.target.password.value;

      const token = await getAuthToken(username, password);
      if (token) {
        alert("Login successful!");
        redirectTo("/index.html");
      } else {
        alert("Invalid credentials");
      }
    });
  }

  // SIGNUP
  if (isSignupPage) {
    const signupForm = document.getElementById("signup-form");
    signupForm?.addEventListener("submit", async e => {
      e.preventDefault();
      const { username, email, password, 'confirm-password': confirm } = e.target.elements;

      if (password.value !== confirm.value) {
        alert("Passwords do not match");
        return;
      }

      const res = await fetch("http://127.0.0.1:8000/api/signup/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          username: username.value,
          email: email.value,
          password: password.value
        })
      });

      const data = await res.json();
      if (res.ok) {
        alert("Signup successful. Please login.");
        redirectTo("/pages/login.html");
      } else {
        alert(data.detail || "Signup failed.");
      }
    });
  }

  // INDEX PAGE
  if (isIndexPage) {
    console.log("Welcome to the dashboard.");
    await renderTicketCounts();
    await renderTickets(3); 
    
  }

// CREATE TICKET
if (isCreateTicketPage) {
  const form = document.getElementById("create-ticket-form");
  form?.addEventListener("submit", async e => {
    e.preventDefault();
    const {
      customer_name,
      email,
      title,
      issue_description,
      priority,
      assigned_to
    } = e.target.elements;

    const success = await createTicket({
      customer_name: customer_name.value,
      email: email.value,
      title: title.value,
      issue_description: issue_description.value,
      priority: priority.value,
      assigned_to: assigned_to.value
    });

    if (success) {
      alert("Ticket created successfully.");
      redirectTo("/pages/ticket-list.html");
    } else {
      alert("Failed to create ticket.");
    }
  });
}

  // TICKET LIST
  if (isTicketListPage) {
    await renderTickets();
  }

  // TICKET DETAIL PAGE
  if (isTicketCardPage) {
    await renderTicketDetails();
  }
});
