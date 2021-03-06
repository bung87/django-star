(function() {
    jQuery.fn.djangoStar = function(config) {
        $(this).each( function() {
            $this = $(this);
            config = $.extend(true, {
                'add' : {
                    'caption' : 'add star'
                },
                'popup' : {
                    'quote' : {
                        'begin' : "\'",
                        'end' : "\'"
                    }
                },
                'del' : {
                    'message' : 'Are you sure you want to delete this star?',
                    'delay' : 2000
                }
            }, config);
            var $container = $('<ul>').addClass('django-star-container');
            var object_id = $this.attr('object-id');
            var content_type = $this.attr('content-type');
            var url = $this.attr('api-url');
            var logged_in = config.logged_in === 'True';
            if(logged_in) {
                var $addButton = $('<li>').addClass('django-star-add-button').append($('<a>')
                .attr('href', 'javascript:void(0)').bind('click', function() {
                    // this code may not work well on IE.
                    var comment = window.getSelection().toString();
                    $.post(url, {
                        comment : comment
                    }, function(data) {
                        $container.append(createStar(data).fadeIn('slow'))
                    }, 'json');
                    return 0;
                }).attr('title', config.add.caption));
                $container.append($addButton);
            }

            var createStar = function(data) {
                var username = data.author.username;
                var user_id = parseInt(data.author.id);
                var comment = data.comment;
                var $star = $('<li>');
                var $popup = $('<div>').addClass('django-star-popup');
                $popup.append(username);
                if(comment) {
                    $popup.append($('<blockquote>').append(config.popup.quote.begin + comment + config.popup.quote.end));
                }
                if(data.tag) {
                    $star.addClass('django-star-tag-' + data.tag);
                }
                $star.attr({
                    'comment' : comment,
                    'username' : username,
                    'star-id' : data.pk
                }).bind('mouseover', function(event) {
                    $star.append($popup.fadeIn('fast'));
                    $popup.css({
                        'top' : event.pageY + 20,
                        'left' : event.pageX + 20
                    })
                    if(logged_in && parseInt(config.user_id) === user_id) {
                        $(this).animate({
                            'opacity' : 1
                        }, config.del.delay, function() {
                            $popup.remove();
                            if(confirm(config.del.message)) {
                                var id = $star.attr('star-id');
                                $.ajax({
                                    'url' : url + id + '/',
                                    'type' : 'DELETE',
                                    'success' : function(data) {
                                        $star.toggle('slow', function() {
                                            $(this).remove();
                                        });
                                    }
                                })
                            }
                        });
                    }
                }).bind('mouseout', function(event) {
                    $(this).stop();
                    $popup.fadeOut('fast', function() {
                        $(this).remove();
                    });
                });
                return $star;
            }
            $this.append($container);
            $.getJSON(url, function(data) {
                var nocomments = {};
                $(data.objects).each( function() {
                    if(this.comment == '') {
                        if(!nocomments[this.author.username]) {
                            nocomments[this.author.username] = 1;
                            $container.append(createStar(this));
                        } else {
                            nocomments[this.author.username] += 1;
                        }
                    } else {
                        $container.append(createStar(this));
                    }
                });
                $.each(nocomments, function(key, value) {
                    if(value > 1) {
                        var $star = $container.find('li[comment=\"\"][username=\"' + key + '\"]');
                        $star.after($('<div>').addClass('django-star-counter').text(value));
                    }
                });
            });
        });
    };
})(jQuery);