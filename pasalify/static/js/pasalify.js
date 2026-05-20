// Pasalify — Client-Side Helpers

// Auto-dismiss alerts after 4 seconds
document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".alert").forEach(el => {
        setTimeout(() => {
            el.style.transition = "opacity .5s";
            el.style.opacity    = "0";
            setTimeout(() => el.remove(), 500);
        }, 4000);
    });

    // Confirm delete buttons
    document.querySelectorAll("form button.btn-danger").forEach(btn => {
        btn.addEventListener("click", e => {
            if (!confirm("Are you sure?")) e.preventDefault();
        });
    });
});
