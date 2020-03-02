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
        nav_toggle();
    });
    $("#wrap main").click(function (e) {
        $(".toggleMenu").removeClass("open_menu");
        $('.toggleMenu .show__menu').css('display', 'inline-block');
        $('.toggleMenu .hide__menu').css('display', 'none');
        $(".nav").hide();
    });

    function nav_toggle() {
        if ($(".toggleMenu").hasClass("open_menu")) {

            $(".toggleMenu").removeClass("open_menu");
            $('.toggleMenu .show__menu').css('display', 'inline-block');
            $('.toggleMenu .hide__menu').css('display', 'none');
            // $('body').css({
            //     'overflow': 'auto',
            //     'position': 'relative'
            // });

            $(".nav").hide();

        } else {

            $(".toggleMenu").addClass("open_menu");
            $('.toggleMenu .show__menu').css('display', 'none');
            $('.toggleMenu .hide__menu').css('display', 'inline-block');
            // $('body').css({
            //     'overflow': 'hidden',
            //     'position': 'relative'
            // });

            $(".nav").show();
        }
    }

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



/*=====
200202追記分
=====*/

$(function() {


    //ポップアップバナーが表示されるまでの時間をミリ秒単位で指定
    var app_popup_delay = 3000;
    //カバー画像がスライドする間隔時間をミリ秒単位で指定
    var img_slide_delay = 6000;



    // ページ表示3秒後にポップアップを表示
    setTimeout(function() {
        $('#app_popup').animate({
            'top': 0
        }, 500, 'swing');
    }, app_popup_delay);

    // ポップアップ非表示処理
    $('.app_popup_close').click(function() {
        $('#app_popup').animate({
            'top': -200
        }, 500, 'swing');
    });


    // カバーmodal表示
    $(document).on('click', '.profile_cover_img img', function() {
        var cover_img = $(this).attr('src');
        $('.profile_cover_modal img').attr('src',cover_img);
        $('.profile_cover_modal').fadeIn();
    });
    // カバーmodal非表示
    $(document).on('click', '.profile_cover_modal', function() {
        $(this).fadeOut();
        setTimeout(function() {
            $('.profile_cover_modal img').attr('src','');
        }, 500);
    });


    // ミニアイコンをクリックしたら画像が切り替わる処理
    $('.profile_cover_select li').each(function() {
        var img = $(this).html();
        $('.profile_cover_img_slide').append(img);
    });

    $('.profile_cover_select li').click(function() {
        var index = $('.profile_cover_select li').index(this);

        $('.profile_cover_img_slide img').stop(true, false).fadeOut();
        $('.profile_cover_img_slide img').eq(index).stop(true, false).fadeIn();
    });

    // カバー自動スライド処理
    var slide_class_check = $('div').hasClass('profile_cover_img_slide');
    $('.profile_cover_select li').eq(0).addClass('active');

    if( slide_class_check ) {
        var slide_num = $('.profile_cover_select li').length;

        setInterval(function() {
            var slide_active = $('.profile_cover_select li').index($('.profile_cover_select li.active'));
            slide_active = slide_active + 1;

            $('.profile_cover_img_slide img').stop(true, false).fadeOut();

            if (slide_num == slide_active) {
                $('.profile_cover_img_slide img').eq(0).stop(true, false).fadeIn();
                $('.profile_cover_select li.active').removeClass('active');
                $('.profile_cover_select li').eq(0).addClass('active');
            } else {
                $('.profile_cover_img_slide img').eq(slide_active).stop(true, false).fadeIn();
                $('.profile_cover_select li.active').removeClass('active').next().addClass('active');
            }

        }, img_slide_delay);
    }
    
});