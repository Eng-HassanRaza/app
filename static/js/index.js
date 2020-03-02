$(document).ready(function () {
    $('.btn__follow').click(function () {
        let old_text = '+ フォロー';
        $(this).toggleClass('active');
        if ($(this).hasClass('active')) {
            $(this).text('フォロー中');
        } else {
            $(this).text(old_text);
        }

    });

    $('.btn__favorite, .btn_follow').click(function () {
        $(this).toggleClass('active');
    });

    $('.tabs .tab__link').click(function () {
        var tab_id = $(this).attr('data-tab');
        $('.tabs .tab__link').removeClass('current');
        $('.tab__content').removeClass('current');
        $(this).addClass('current');
        $("#" + tab_id).addClass('current');
    });

    function leanpro_init_carousel() {
        $('.owl-slick').not('.slick-initialized').each(function () {
            var _this = $(this),
                _responsive = _this.data('responsive'),
                _slick = _this.data('slick'),
                _config = [];
            if (typeof _slick == "object") {
                _config = _slick;
            }
            if (_this.hasClass('slick-vertical')) {
                _config.prevArrow = '<span class="pe-7s-angle-up"></span>';
                _config.nextArrow = '<span class="pe-7s-angle-down"></span>';
            } else {
                _config.prevArrow = '<span class="fa fa-angle-left pre"></span>';
                _config.nextArrow = '<span class="fa fa-angle-right next"></span>';
            }
            _config.responsive = _responsive;
            _this.slick(_config);
        });
    }
    leanpro_init_carousel();


    $('.slick-carousel').slick({
        slidesToShow: 1,
        dots: true,
        arrows: false
    });
});

$(window).on('load', function () {
    $('.menu__tabicon, .btn__share').click(function () {
        $('.share').toggleClass('open');
        $('.location').css('z-index', 1);
    });

    $('.menu__tabicon').click(function () {
        $(this).toggleClass('active');
    });

    $('.overlay').click(function () {
        $('.share').removeClass('open');
        $('.menu__tabicon').removeClass('active');
        $('.location').css('z-index', 10);
    });

    if ($('.share').hasClass('open')) {
        $('.location').css('z-index', 1);
    }
});

$(document).ready(function () {
    var sel = $('.select__box'),
        txt = $('.select__current'),
        options = $('.select__options');

    txt.click(function () {
        options.toggleClass('show__lang');
    });

    options.children('div').click(function (e) {
        e.stopPropagation();
        txt.text($(this).text());
        $(this).addClass('selected').siblings('div').removeClass('selected');
        options.removeClass('show__lang');
    });
});

$(document).ready(function () {
    $(".toggleMenu").click(function (e) {
        if ($(".toggleMenu").hasClass("open_menu")) {

            $(".toggleMenu").removeClass("open_menu");
            $('.toggleMenu .show__menu').css('display', 'inline-block');
            $('.toggleMenu .hide__menu').css('display', 'none');
            $('body').css({
                'overflow': 'auto',
                'position': 'relative'
            });

            $(".nav").hide();

        } else {

            $(".toggleMenu").addClass("open_menu");
            $('.toggleMenu .show__menu').css('display', 'none');
            $('.toggleMenu .hide__menu').css('display', 'inline-block');
            $('body').css({
                'overflow': 'hidden',
                'position': 'relative'
            });

            $(".nav").show();
        }
    });

    $(".nav").hide();
})


$(document).ready(function () {
    var top = $('.sticky-scroll-box').offset().top;
    var social_menu = $('.box-icon').offset().top;

    $(window).scroll(function (event) {
        var y = $(this).scrollTop();
        if (y >= top) {
            $('.sticky-scroll-box').addClass('fixed');
        } else {
            $('.sticky-scroll-box').removeClass('fixed');
        }
    });

    if (navigator.userAgent.match(/(iPod|iPhone|iPad)/)) {
        $(window).scroll(function (event) {
            var y = $(this).scrollTop();
            if (y >= social_menu) {
                $('.box-icon').addClass('fixed');
            } else {
                $('.box-icon').removeClass('fixed');
            }
        });
    }
});