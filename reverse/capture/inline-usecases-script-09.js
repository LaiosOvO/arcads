

$(document).ready(function() {
    $(".testimonial_filter-button-content").click(function() {
        if ($(this).hasClass("is-clear")) {
            if ($(this).hasClass("is-active")) {
                $(this).removeClass("is-active");
            } else {
                $(".testimonial_filter-button-content").removeClass("is-active");
                $(this).addClass("is-active");
            }
        } else {
            $(".testimonial_filter-button-content").removeClass("is-active");
        }
    });
});
