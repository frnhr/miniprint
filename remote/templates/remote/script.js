jQuery(function($){
    {% if checkbox_name %}
    var $checkbox = $('<input type="checkbox" name="{{ checkbox_name|escapejs }}" />');
    {% else %}
    var $checkbox = '';
    {% endif %}
    var $before_link = '<span class="fineprint_before_link">{{ before_link|escapejs }}</span>';
    var $after_link = '<span class="fineprint_after_link">{{ after_link|escapejs }}</span>';
    var $link = $('<a href="">terms and conditions</a>');
    $miniprint_container = $('#miniprint_container');
    $miniprint_container
        .append($checkbox)
        .append($before_link)
        .append($link)
        .append($after_link);

    $link.on('click', function(event){
        event.preventDefault();
        window.open(
            "http://en.wikipedia.org/wiki/Cross-site_scripting",
            "_blank",
            "toolbar=no, scrollbars=yes, resizable=yes, top=50, left=100, width=700, height=600"
        );
    });

    $checkbox.on('change', function(){
        var val = $(this).is(':checked');
        var url = '{{ remote_check_url }}?document_id={{ document_id }}&val=' + val;
        $miniprint_container.append('<script src="' + url + '"></script>');
    });
});
