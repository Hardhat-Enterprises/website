$(document).ready(function() {
    $('#load-more-btn').click(function() {
        var page = $(this).data('page');

        
        $('#loading-indicator').show();

        $.ajax({
            url: load_more_url, 
            type: 'GET',
            data: {
                'page': page
            },
            success: function(data) {
                if (data.posts_html) {
                    $('#post-container').append(data.posts_html);
                }

                if (!data.has_next) {
                    $('#load-more-btn').prop('disabled', true).text('No More Posts');
                } else {
                    $('#load-more-btn').data('page', page + 1);
                }
            },
            error: function(xhr, status, error) {
                console.log('Error loading more posts:', error);
            },
            complete: function() {
                
                $('#loading-indicator').hide();
            }
        });
    });
});