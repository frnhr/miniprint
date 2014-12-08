
jQuery(function($){

    var get_csrf_token = function() {
        return $('#csrf_token').find('input').val();
    };

    var post_a_vote = function(target_model, target_id, score) {
        var urls = {
            'chunk': '{% url "vote_chunk_api" %}',
            'comment': '{% url "vote_comment_api" %}'
        };
        return $.ajax(
            urls[target_model],
            {
                headers: {
                    'X-csrftoken': get_csrf_token()
                },
                cache: false,
                data: {
                    'target_id': target_id,
                    'score': score
                },
                type: 'POST'
            }
        );
    };

    $('.vote_link').on('click', function(event){
        event.preventDefault();
        var $this = $(this);
        var voted_this = $this.hasClass('voted_this');
        var score = $this.data('score');
        if (voted_this) {
            score = 0;
        }
        var target_model = $this.data('target_model');
        var target_id = parseInt($this.data('target_id'));
        post_a_vote(target_model, target_id, score)
            .done(function(){alert("done")})
            .fail(function(){alert("fail")})
        ;

        // todo uncheck pair link
    });
});