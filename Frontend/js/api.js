const apiBaseUrl = "http://127.0.0.1:8000/";
const tokenUrl = `${apiBaseUrl}api/token/`;
const ticketsUrl = `${apiBaseUrl}api/tickets/`;
const aiApiUrl = `${apiBaseUrl}api/ai_recommendation/`;

/**
 * Get AI recommendation based on ticket description.
 * Updates the DOM element with id="ai-recommendations".
 */
async function getAIRecommendation(ticketDescription) {
    const token = localStorage.getItem("authToken"); // ✅ Grab the token
  
    try {
      const response = await fetch(aiApiUrl, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}` // ✅ Send token for auth
        },
        body: JSON.stringify({ description: ticketDescription })
      });
  
      const data = await response.json();
      console.log("AI Recommendation response:", data);
  
      const aiBox = document.getElementById("ai-recommendations");
      if (response.ok && data.recommendation) {
        aiBox.innerText = data.recommendation;
      } else {
        aiBox.innerText = "No recommendation found.";
      }
    } catch (error) {
      console.error("Error fetching AI recommendations:", error);
      const aiBox = document.getElementById("ai-recommendations");
      if (aiBox) {
        aiBox.innerText = "Error fetching AI recommendations.";
      }
    }
  }

// Trigger AI recommendation 
function onTicketSelect(ticketDescription) {
  getAIRecommendation(ticketDescription);
}

/**
 * Get JWT auth token using username and password.
 */
async function getAuthToken(username, password) {
  try {
    const response = await fetch(tokenUrl, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password })
    });

    if (!response.ok) throw new Error("Invalid credentials");

    const { access, refresh } = await response.json();

    localStorage.setItem("authToken", access);
    localStorage.setItem("refreshToken", refresh);

    return access;
  } catch (error) {
    console.error("Error fetching auth token:", error);
    return null;
  }
}

/**
 * Fetch all tickets for the authenticated user.
 */
async function fetchTickets(authToken) {
  try {
    const response = await fetch(ticketsUrl, {
      method: "GET",
      headers: {
        "Authorization": `Bearer ${authToken}`,
        "Content-Type": "application/json"
      }
    });

    if (!response.ok) throw new Error(`Failed to fetch tickets: ${response.status}`);
    
    const tickets = await response.json();

    // Normalize status casing
    tickets.forEach(ticket => {
        if (ticket.status) {
          ticket.status_display = ticket.status
            .replace(/_/g, ' ')
            .split(' ')
            .map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
            .join(' ');
        }
      });

    return tickets;
  } catch (error) {
    console.error("Error fetching tickets:", error);
    return [];
  }
}

async function createTicket(ticketData) {
    try {
      const authToken = localStorage.getItem("authToken");
      if (!authToken) {
        console.error("No auth token found — user may need to log in.");
        return false;
      }

      // Log ticket data for debugging purposes
      console.log("Ticket Data: ", ticketData);

      // Check if assigned_to is included in ticketData
      if (!ticketData.assigned_to) {
        console.error("Assigned technician not specified.");
        return false;
      }

      const response = await fetch(ticketsUrl, {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${authToken}`,
          "Content-Type": "application/json"
        },
        body: JSON.stringify(ticketData)
      });

      if (!response.ok) {
        const contentType = response.headers.get("Content-Type") || "";
        if (contentType.includes("application/json")) {
          const errorData = await response.json();
          console.error("Failed to create ticket:", errorData);
        } else {
          const errorText = await response.text();
          console.error("Failed to create ticket. Server responded with HTML:", errorText);
        }
        return false;
      }

      return await response.json();
    } catch (error) {
      console.error("Error creating ticket:", error);
      return false;
    }
}


// Export functions for use in other files
export {
  getAuthToken,
  fetchTickets,
  createTicket,
  getAIRecommendation
};
