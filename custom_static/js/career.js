document.addEventListener("DOMContentLoaded", function () {
    // Job Alert Subscription
    const jobAlertForm = document.getElementById("jobAlertForm");

    if (jobAlertForm) {
        jobAlertForm.addEventListener("submit", function (e) {
            e.preventDefault();
            const email = document.getElementById("jobAlertEmail").value;
            if (email) {
                localStorage.setItem("jobAlertEmail", email);
                document.getElementById("jobAlertMessage").style.display = "block";
            }
        });
    }

    // Testimonial Carousel
    const testimonials = [
        "“Hardhat Enterprises gave me great career growth opportunities.”",
        "“I love the team culture—everyone is so supportive!”",
        "“A fantastic place to work if you're passionate about cybersecurity!”"
    ];

    let currentTestimonial = 0;

    function updateTestimonial() {
        document.getElementById("testimonial-text").innerText = testimonials[currentTestimonial];
    }

    document.getElementById("nextTestimonial")?.addEventListener("click", function () {
        currentTestimonial = (currentTestimonial + 1) % testimonials.length;
        updateTestimonial();
    });

    document.getElementById("prevTestimonial")?.addEventListener("click", function () {
        currentTestimonial = (currentTestimonial - 1 + testimonials.length) % testimonials.length;
        updateTestimonial();
    });

    updateTestimonial();
});
