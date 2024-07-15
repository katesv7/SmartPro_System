// static/js/script.js

$(document).ready(function() {
    // Handle feedback form submission
    $('#feedbackForm').on('submit', function(event) {
        event.preventDefault();
        
        const data = {
            student_id: $('#studentId').val(),
            element_name: $('#elementName').val(),
            rating: $('#rating').val(),
            comment: $('#comment').val()
        };

        $.ajax({
            url: '/submit_feedback',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(data),
            success: function(response) {
                alert(response.message);
                $('#feedbackForm')[0].reset();
            },
            error: function(xhr) {
                alert(xhr.responseJSON.error);
            }
        });
    });

    // Handle view feedback form submission
    $('#viewFeedbackForm').on('submit', function(event) {
        event.preventDefault();
        
        const elementName = $('#viewElementName').val();

        $.ajax({
            url: '/view_feedback',
            type: 'GET',
            data: { element_name: elementName },
            success: function(response) {
                let feedbackList = '<ul class="list-group">';
                response.forEach(function(feedback) {
                    feedbackList += `<li class="list-group-item">
                        <strong>Student ID:</strong> ${feedback.student_id}<br>
                        <strong>Rating:</strong> ${feedback.rating}<br>
                        <strong>Comment:</strong> ${feedback.comment}<br>
                        <strong>Date:</strong> ${feedback.date}
                    </li>`;
                });
                feedbackList += '</ul>';
                $('#feedbackList').html(feedbackList);
            },
            error: function(xhr) {
                alert(xhr.responseJSON.error);
            }
        });
    });

    // Handle generate report button click
    $('#generateReport').on('click', function() {
        $.ajax({
            url: '/generate_report',
            type: 'GET',
            success: function(response) {
                let report = '<ul class="list-group">';
                for (const [element, data] of Object.entries(response)) {
                    report += `<li class="list-group-item">
                        <strong>Element Name:</strong> ${element}<br>
                        <strong>Total Feedbacks:</strong> ${data.total_feedbacks}<br>
                        <strong>Average Rating:</strong> ${data.average_rating.toFixed(2)}
                    </li>`;
                }
                report += '</ul>';
                $('#report').html(report);
            },
            error: function(xhr) {
                alert('Error generating report.');
            }
        });
    });
});
