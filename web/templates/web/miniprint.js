
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
        var $wrap = $this.parents('.vote_wrap');
        var voted_this = $this.hasClass('voted_this');
        var score = $this.data('score');
        if (voted_this) {
            score = 0;
        }
        var target_model = $this.data('target_model');
        var target_id = parseInt($this.data('target_id'));
        $wrap.find('.voted_this').removeClass('voted_this');
        if (score == $this.data('score'))
            $this.addClass('voted_this');
        post_a_vote(target_model, target_id, score)
            .done(function(data){
                console.info(data);
                console.info($wrap);
                $wrap.find('.score').text(data['target_score']);
            })
            .fail(function(){
                $this.removeClass('voted_this');
            })
        ;
    });
});