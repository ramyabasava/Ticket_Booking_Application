// This function will be called from the confirmation.html page
function showConfirmationAlert(userName, numTickets, eventName) {
    // Wait for the page to be fully loaded before showing the alert
    window.onload = () => {
        const message = `🎉 Thank you, ${userName}! 🎉\n\nYour booking for ${numTickets} ticket(s) to "${eventName}" is confirmed.\n\nA confirmation email has been sent (for demo purposes).`;
        alert(message);
    };
}