(function ($) {
    "use strict";

    $(window).on('load', function () {
        $('#preloader').fadeOut('slow', function () { $(this).remove(); });
    });
    $(window).on("scroll", function () {
        if ($(this).scrollTop() > 200) {
            $('.scrollup').fadeIn();
        } else {
            $('.scrollup').fadeOut();
        }
    });

    var dateRangePicker = $('input[name="daterange"]');

    if ($(dateRangePicker).length) {
        $('#fromDate, #toDate').daterangepicker({
            singleDatePicker: true,
            startDate: moment().subtract(6, 'days')
        });

        $(dateRangePicker).daterangepicker({
            opens: 'right',
            format: 'DD-MM-YYYY'
        });
    }

    $('.scrollup').on("click", function () {
        $("html, body").animate({
            scrollTop: 0
        }, 800);
        return false;
    });
    if ($('select').length) {
        $(document).ready(function () {
            $('select').niceSelect();
        });
    };

    if ($(".cursor-overlay").length) {
        // / cursor /
        var cursor = $(".cursor-overlay .cursor"),
            follower = $(".cursor-overlay .cursor-follower");

        var posX = 0,
            posY = 0;

        var mouseX = 0,
            mouseY = 0;

        TweenMax.to({}, 0.016, {
            repeat: -1,
            onRepeat: function () {
                posX += (mouseX - posX) / 9;
                posY += (mouseY - posY) / 9;

                TweenMax.set(follower, {
                    css: {
                        left: posX - 22,
                        top: posY - 22
                    }
                });

                TweenMax.set(cursor, {
                    css: {
                        left: mouseX,
                        top: mouseY
                    }
                });
            }
        });

        $(document).on("mousemove", function (e) {
            var scrollTop =
                window.pageYOffset || document.documentElement.scrollTop;
            mouseX = e.pageX;
            mouseY = e.pageY - scrollTop;
        });
        $("button, a").on("mouseenter", function () {
            cursor.addClass("active");
            follower.addClass("active");
        });
        $("button, a").on("mouseleave", function () {
            cursor.removeClass("active");
            follower.removeClass("active");
        });
        $(".cursor-overlay").on("mouseenter", function () {
            cursor.addClass("close-cursor");
            follower.addClass("close-cursor");
        });
        $(".cursor-overlay").on("mouseleave", function () {
            cursor.removeClass("close-cursor");
            follower.removeClass("close-cursor");
        });
    }

    /* ------------------ OWL CAROUSEL ------------------ */

    var $carouselDirection = $("html").attr("dir");
    if ($carouselDirection == "rtl") {
        var $carouselrtl = true;
    } else {
        var $carouselrtl = false;
    }

    $(".carousel").each(function () {
        var $Carousel = $(this);
        $Carousel.owlCarousel({
            loop: $Carousel.data('loop'),
            autoplay: $Carousel.data("autoplay"),
            margin: $Carousel.data('space'),
            nav: $Carousel.data('nav'),
            dots: $Carousel.data('dots'),
            center: $Carousel.data('center'),
            dotsSpeed: $Carousel.data('speed'),
            animateOut: 'fadeOut',
            responsive: {
                0: {
                    items: 1,
                },
                600: {
                    items: $Carousel.data('slide-rs'),
                },
                1000: {
                    items: $Carousel.data('slide'),
                }
            }
        });
    });
    /*
    //three-item-carousel
    if ($('.testimonial-slide').length) {
        $('.testimonial-slide').owlCarousel({
            loop: true,
            margin: 30,
            nav: true,
            smartSpeed: 1000,
            autoplay: 500,
            navText: ['<span class="fa fa-arrow-left"></span>', '<span class="fa fa-arrow-right"></span>'],
            responsive: {
                0: {
                    items: 1
                },
                480: {
                    items: 1
                },
                600: {
                    items: 1
                },
                800: {
                    items: 1
                },
                1024: {
                    items: 1
                }
            }
        });
    }
    */
    $('[data-background]').each(function () {
        $(this).css('background-image', 'url(' + $(this).attr('data-background') + ')');
    });
    if ($(".odometer").length) {
        $('.odometer').appear();
        $(document.body).on('appear', '.odometer', function (e) {
            var odo = $(".odometer");
            odo.each(function () {
                var countNumber = $(this).attr("data-count");
                $(this).html(countNumber);
            });
        });
    };

    if ($(".search-popup-toggler").length) {
        $(".search-popup-toggler").on("click", function (e) {
            $(".search-popup").addClass("active");
            e.preventDefault();
        });
    }

    if ($(".search-popup-overlay").length) {
        $(".search-popup-overlay").on("click", function (e) {
            $(".search-popup").removeClass("active");
            e.preventDefault();
        });
    }

    $('#main-slider-3').owlCarousel({
        items: 1,
        loop: true,
        nav: true,
        dots: false,
        autoplay: true,
        navSpeed: 1000,
        smartSpeed: 2000,
        navText: ["<i class='fas fa-arrow-left'></i>", "<i class='fas fa-arrow-right'></i>"],
    });
    $(window).on('load', function () {
        $('.top-category-slider').owlCarousel({
            margin: 30,
            responsiveClass: true,
            nav: true,
            dots: false,
            navText: ["<i class='fas fa-chevron-left'></i>", "<i class='fas fa-chevron-right'></i>"],
            loop: true,
            responsive: {
                0: {
                    items: 1,
                },
                400: {
                    items: 1,
                },
                600: {
                    items: 2,
                },
                700: {
                    items: 2,
                },
                1000: {
                    items: 3,

                },
                1300: {
                    items: 4,

                },
                1900: {
                    items: 4,
                },
            },
        })
    });
    if ($(".odometer").length) {
        $('.odometer').appear();
        $(document.body).on('appear', '.odometer', function (e) {
            var odo = $(".odometer");
            odo.each(function () {
                var countNumber = $(this).attr("data-count");
                $(this).html(countNumber);
            });
        });
    };
    $(window).on('load', function () {
        $('.testimonial-slider-3').owlCarousel({
            margin: 30,
            responsiveClass: true,
            nav: false,
            dots: true,
            loop: true,
            responsive: {
                0: {
                    items: 1,
                },
                400: {
                    items: 1,
                },
                600: {
                    items: 1,
                },
                700: {
                    items: 2,
                },
                1000: {
                    items: 2,

                },
                1300: {
                    items: 3,

                },
                1900: {
                    items: 3,
                },
            },
        })
    });

    if ($('.wow').length) {
        var wow = new WOW(
            {
                boxClass: 'wow',
                animateClass: 'animated',
                offset: 0,
                mobile: true,
                live: true
            }
        );
        wow.init();
    };

    //three-item-carousel
    if ($('.testimonial-featured-slide').length) {
        $('.testimonial-featured-slide').owlCarousel({
            loop: true,
            margin: 30,
            nav: true,
            smartSpeed: 1000,
            autoplay: 500,
            navText: ['<span class="fa fa-arrow-left"></span>', '<span class="fa fa-arrow-right"></span>'],
            responsive: {
                0: {
                    items: 1
                },
                480: {
                    items: 1
                },
                600: {
                    items: 2
                },
                800: {
                    items: 2
                },
                1024: {
                    items: 2
                }
            }
        });
    }

    if ($(".details-area-slide-carousel").length) {
        $(".details-area-slide-carousel").each(function () {
            var Self = $(this);
            var carouselOptions = Self.data("options");
            var carouselPrevSelector = Self.data("carousel-prev-btn");
            var carouselNextSelector = Self.data("carousel-next-btn");
            var thmCarousel = Self.owlCarousel(carouselOptions);
            if (carouselPrevSelector !== undefined) {
                $(carouselPrevSelector).on("click", function () {
                    thmCarousel.trigger("prev.owl.carousel");
                    return false;
                });
            }
            if (carouselNextSelector !== undefined) {
                $(carouselNextSelector).on("click", function () {
                    thmCarousel.trigger("next.owl.carousel");
                    return false;
                });
            }
        });
    };


    if ($('.video-box').length) {
        $('.video-box').fancybox({
            openEffect: 'fade',
            closeEffect: 'fade',
            helpers: {
                media: {}
            }
        });
    };

    $(window).on('scroll', function () {
        if ($(window).scrollTop() > 100) {
            $('.header-main').addClass('sticky-menu')
        } else {
            $('.header-main').removeClass('sticky-menu')
        }
    });


    $('.nav-mobile-menu').on("click", function () {
        $('.mobile-menu-navbar').toggleClass("mobile-menu-on");
    });
    $('.nav-mobile-menu').on('click', function () {
        $('body').toggleClass('mobile-menu-overlay-on');
    });
    if ($('.mobile-menu li.dropdown ul').length) {
        $('.mobile-menu li.dropdown').append('<div class="dropdown-btn"><span class="fa fa-angle-down"></span></div>');
        $('.mobile-menu li.dropdown .dropdown-btn').on('click', function () {
            $(this).prev('ul').slideToggle(500);
        });
    };


    $('#main-slider').owlCarousel({
        items: 1,
        loop: true,
        nav: false,
        dots: true,
        autoplay: true,
        navSpeed: 2000,
        smartSpeed: 3000,
        animateOut: 'fadeOut',
        animateIn: 'fadeIn',
    });
    $('#main-slider-2').owlCarousel({
        items: 1,
        loop: true,
        nav: true,
        dots: false,
        autoplay: true,
        navSpeed: 1000,
        smartSpeed: 2000,
        navText: ["<i class='fas fa-arrow-left'></i>", "<i class='fas fa-arrow-right'></i>"],
    });
    $('#activity-slider-2').owlCarousel({
        items: 1,
        loop: true,
        nav: true,
        dots: false,
        autoplay: true,
        navSpeed: 1000,
        smartSpeed: 2000,
        navText: ["<i class='fas fa-arrow-left'></i>", "<i class='fas fa-arrow-right'></i>"],
    });


    $(window).on('load', function () {
        $('#activity-type-slider').owlCarousel({
            margin: 30,
            responsiveClass: true,
            nav: true,
            dots: false,
            navText: ["<i class='fas fa-arrow-left'></i>", "<i class='fas fa-arrow-right'></i>"],
            loop: true,
            responsive: {
                0: {
                    items: 1,
                },
                400: {
                    items: 1,
                },
                600: {
                    items: 1,
                },
                700: {
                    items: 2,
                },
                1000: {
                    items: 3,

                },
                1300: {
                    items: 3,

                },
                1900: {
                    items: 3,

                },
            },
        })
    });

    $(window).on('load', function () {
        $('#activity-featured-slider').owlCarousel({
            margin: 30,
            responsiveClass: true,
            nav: true,
            dots: false,
            navText: ["<i class='fas fa-arrow-left'></i>", "<i class='fas fa-arrow-right'></i>"],
            loop: true,
            responsive: {
                0: {
                    items: 1,
                },
                400: {
                    items: 1,
                },
                600: {
                    items: 1,
                },
                700: {
                    items: 2,
                },
                1000: {
                    items: 3,

                },
                1300: {
                    items: 3,

                },
                1900: {
                    items: 3,

                },
            },
        })
    });

    $(window).on('load', function () {
        $('#activity-featured-slider-2').owlCarousel({
            margin: 30,
            responsiveClass: true,
            nav: true,
            dots: false,
            navText: ["<i class='fas fa-arrow-left'></i>", "<i class='fas fa-arrow-right'></i>"],
            loop: true,
            responsive: {
                0: {
                    items: 1,
                },
                400: {
                    items: 1,
                },
                600: {
                    items: 1,
                },
                700: {
                    items: 2,
                },
                1000: {
                    items: 3,

                },
                1300: {
                    items: 4,

                },
                1900: {
                    items: 4,

                },
            },
        })
    });

    $(window).on('load', function () {
        $('#activity-featured-slider-3').owlCarousel({
            margin: 30,
            responsiveClass: true,
            nav: true,
            dots: false,
            navText: ["<i class='fas fa-arrow-left'></i>", "<i class='fas fa-arrow-right'></i>"],
            loop: true,
            responsive: {
                0: {
                    items: 1,
                },
                400: {
                    items: 1,
                },
                600: {
                    items: 1,
                },
                700: {
                    items: 2,
                },
                1000: {
                    items: 2,

                },
                1300: {
                    items: 2,

                },
                1900: {
                    items: 2,

                },
            },
        })
    });


    /*
    $(window).on('load', function () {
        $('#testimonial-featured-slider').owlCarousel({
            margin: 30,
            responsiveClass: true,
            nav: true,
            dots: false,
            navText: ["<i class='fas fa-arrow-left'></i>", "<i class='fas fa-arrow-right'></i>"],
            loop: true,
            responsive: {
                0: {
                    items: 1,
                },
                400: {
                    items: 1,
                },
                600: {
                    items: 1,
                },
                700: {
                    items: 2,
                },
                1000: {
                    items: 2,

                },
                1300: {
                    items: 2,

                },
                1900: {
                    items: 2,

                },
            },
        })
    });
    */
    var e = $(".image-grid"); if (e.length) var o = e.imagesLoaded(function () { o.masonry({ percentPosition: !0, itemSelector: ".image-grid-item" }) });

    $(window).on('load', function () {
        $('#testimonial-slide').owlCarousel({
            margin: 0,
            items: 1,
            nav: false,
            dots: true,
            loop: true,
        })
    });


    $(window).on('load', function () {
        // Testimonials Slider
        $('.testimonials-slider').owlCarousel({
            loop: true,
            margin: 30,
            singleItem: true,
            nav: false,
            dots: true,
            smartSpeed: 1000,
            autoplay: false,
            autoplayTimeout: 4000,
            autoplayHoverPause: true,
            responsive: {
                0: {
                    items: 1,
                },
                768: {
                    items: 2,
                },
                992: {
                    items: 2,
                }
            }
        });
    });


    var $grid = $('.grid').imagesLoaded(function () {
        $grid.masonry({
            percentPosition: true,
            itemSelector: '.grid-item',
            columnWidth: '.grid-sizer'
        });
    });


    if ($('.chart_1').length) {
        $('.chart_1').easyPieChart({
            size: 130,
            barColor: '#ff7554',
            trackColor: '#373f4b',
            easing: 'easeOutBounce',
            scaleColor: false,
            lineCap: 'circle',
            lineWidth: 10,
            animate: 2000
        });
    };

    var $grid = $('.grid').imagesLoaded(function () {
        $grid.masonry({
            percentPosition: true,
            itemSelector: '.grid-item',
            columnWidth: '.grid-sizer'
        });
    });
    var $grid = $(".grid").isotope({
        itemSelector: ".grid-item",
        layoutMode: "fitRows"
    });
    var filterFns = {
        numberGreaterThan50: function () {
            var number = $(this)
                .find(".number")
                .text();
            return parseInt(number, 10) > 50;
        },
        ium: function () {
            var name = $(this)
                .find(".name")
                .text();
            return name.match(/ium$/);
        }
    };
    $(".button-group").on("click", "button", function () {
        var filterValue = $(this).attr("data-filter");
        filterValue = filterFns[filterValue] || filterValue;
        $grid.isotope({ filter: filterValue });
    });

    $(".button-group").each(function (i, buttonGroup) {
        var $buttonGroup = $(buttonGroup);
        $buttonGroup.on("click", "button", function () {
            $buttonGroup.find(".is-checked").removeClass("is-checked");
            $(this).addClass("is-checked");
        });
    });

    $(window).on('load', function () {
        $('#blog-slider').owlCarousel({
            margin: 30,
            responsiveClass: true,
            nav: true,
            dots: false,
            navText: ["<i class='fas fa-arrow-left'></i>", "<i class='fas fa-arrow-right'></i>"],
            loop: true,
            responsive: {
                0: {
                    items: 1,
                },
                400: {
                    items: 1,
                },
                600: {
                    items: 1,
                },
                700: {
                    items: 2,
                },
                1000: {
                    items: 3,

                },
                1300: {
                    items: 3,

                },
                1900: {
                    items: 3,
                },
            },
        })
    });


    $(window).on('load', function () {
        $('#category-slide').owlCarousel({
            margin: 30,
            responsiveClass: true,
            nav: false,
            dots: true,
            loop: true,
            responsive: {
                0: {
                    items: 1,
                },
                400: {
                    items: 1,
                },
                600: {
                    items: 1,
                },
                700: {
                    items: 2,
                },
                1000: {
                    items: 3,

                },
                1300: {
                    items: 3,

                },
                1900: {
                    items: 3,
                },
            },
        })
    });


    $(window).on('load', function () {
        $('#testimonial-slide-2').owlCarousel({
            margin: 30,
            responsiveClass: true,
            nav: false,
            dots: true,
            loop: true,
            responsive: {
                0: {
                    items: 1,
                },
                400: {
                    items: 1,
                },
                600: {
                    items: 1,
                },
                700: {
                    items: 2,
                },
                1000: {
                    items: 3,

                },
                1300: {
                    items: 3,

                },
                1900: {
                    items: 3,
                },
            },
        })
    });


    $(window).on('load', function () {
        $('#blog-slider-2').owlCarousel({
            margin: 30,
            responsiveClass: true,
            nav: false,
            dots: true,
            loop: true,
            responsive: {
                0: {
                    items: 1,
                },
                400: {
                    items: 1,
                },
                600: {
                    items: 1,
                },
                700: {
                    items: 2,
                },
                1000: {
                    items: 3,

                },
                1300: {
                    items: 3,

                },
                1900: {
                    items: 3,
                },
            },
        })
    });


    $(window).on('load', function () {
        $('#agent-slider').owlCarousel({
            margin: 30,
            responsiveClass: true,
            nav: true,
            dots: false,
            navText: ["<i class='fas fa-arrow-left'></i>", "<i class='fas fa-arrow-right'></i>"],
            loop: true,
            responsive: {
                0: {
                    items: 1,
                },
                400: {
                    items: 1,
                },
                600: {
                    items: 1,
                },
                700: {
                    items: 2,
                },
                1000: {
                    items: 3,

                },
                1300: {
                    items: 4,

                },
                1900: {
                    items: 4,
                },
            },
        })
    });


    $(window).on('load', function () {
        $('#destination-slider').owlCarousel({
            margin: 30,
            responsiveClass: true,
            nav: true,
            dots: false,
            navText: ["<i class='fas fa-arrow-left'></i>", "<i class='fas fa-arrow-right'></i>"],
            loop: true,
            responsive: {
                0: {
                    items: 1,
                },
                400: {
                    items: 1,
                },
                600: {
                    items: 1,
                },
                700: {
                    items: 2,
                },
                1000: {
                    items: 3,

                },
                1300: {
                    items: 4,

                },
                1900: {
                    items: 4,
                },
            },
        })
    });


    if ($('#google_map').length) {
        var $lat = $('#google_map').data('lat');
        var $lon = $('#google_map').data('lon');
        var $zoom = $('#google_map').data('zoom');
        var $marker = $('#google_map').data('marker');
        var $info = $('#google_map').data('info');
        var $markerLat = $('#google_map').data('mlat');
        var $markerLon = $('#google_map').data('mlon');
        var map = new GMaps({
            el: '#google_map',
            lat: $lat,
            lng: $lon,
            scrollwheel: false,
            scaleControl: true,
            streetViewControl: false,
            panControl: true,
            disableDoubleClickZoom: true,
            mapTypeControl: false,
            zoom: $zoom,
        });
        map.addMarker({
            lat: $markerLat,
            lng: $markerLon,
            icon: $marker,
            infoWindow: {
                content: $info
            }
        })
    };


})(jQuery);
