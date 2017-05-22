// Detect Ie
var detectIe = (function() {
    var ie = 0;
    try { ie = navigator.userAgent.match( /(MSIE |Trident.*rv[ :])([0-9]+)/ )[ 2 ]; }
    catch(e){}
    if (ie !== 0) document.getElementsByTagName("html")[0].className += " ie v" + ie;
 })();

 function htmlToArray(el){
    var arr = [];
    var arrayList = el.children();
    arrayList.each(function(){
        arr.push($(this).text().toLowerCase())
    });
    return arr;
 }

Number.prototype.format = function(n, x) {
    var re = '\\d(?=(\\d{' + (x || 3) + '})+' + (n > 0 ? '\\.' : '$') + ')';
    return this.toFixed(Math.max(0, ~~n)).replace(new RegExp(re, 'g'), '$& ');
};

function getURLParameter(name) {
  return decodeURIComponent((new RegExp('[?|&]' + name + '=' + '([^&;]+?)(&|#|;|$)').exec(location.search) || [null, ''])[1].replace(/\+/g, '%20')) || null;
}

//Get query string parameters

function get_query_value( name, url ) {
    if (!url) url = location.href;
    name = name.replace(/[\[]/,"\\\[").replace(/[\]]/,"\\\]");

    var regexS_attr = "[\\?&]"+name,
        regexS_value = "[\\?&]"+name+"=([^&#]*)",
        regex_attr = new RegExp( regexS_attr ),
        regex_value = new RegExp( regexS_value ),
        results_attr = regex_attr.exec(url),
        results_value = regex_value.exec(url);

    if (results_attr && !results_value){
        return "";
    } else {
        return results_value == null ? null : results_value[1];
    }
}

// Authorization and registration panel module
var AuthPanel = (function() {
    var authPanel = $(".auth-panel");

    var result = {
        init: function(){
            var close = authPanel.find(".js-close");
            if (close.length)
                close.on("click", function(e){
                    result.close();
                });
        },
        show: function(target) {
            var content = authPanel.find(target);
            if (content.length){
                content.siblings(".active").hide().removeClass("active");
                content.addClass("active").fadeIn().css("display","inline-block");
            }

            if (authPanel.is(":hidden"))
                authPanel.fadeIn();
        },
        close: function() {
            if (authPanel.is(":visible"))
                authPanel.fadeOut();
        }
    };
    return result;
})();

// Forms module
var Forms = (function(){
    var forms = $("form");
    var validateForms =$(".form-validate");

    function initValidator(){
        $.validator.addMethod("equal", function(value, element) {
            var equalTo=$($(element).data("equalto"));
            if ( equalTo.not( ".validate-equalTo-blur" ).length ) {
                equalTo.addClass( "validate-equalTo-blur" ).on( "blur.validate-equalTo", function() {
                    $( element ).valid();
                });
            }
            return value === equalTo.val();
        });

        $.validator.addMethod("email", function(value, element) {
            return this.optional(element) || /^[a-zA-Z0-9.!#$%&'*+\/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)+$/.test(value);
        });

        $.validator.addMethod("userName", function(value, element) {
            return this.optional(element) || /^[a-zA-Z0-9-_/.]+$/.test(value);
        });

        $.validator.addMethod("domenName", function(value, element) {
            return this.optional(element) || /^[a-zA-Z][a-zA-Z0-9-]{2,61}[a-zA-Z0-9]$/.test(value);
        });

        $.validator.addMethod("personName", function(value, element) {
            return this.optional(element) || /^[^0-9-_+=\~!@#$%\^\&\*\,\.\?\|\\\/\"\№\;\:\(\)\<\>\{\}\[\]]+$/.test(value);
        });

        $.validator.addMethod("simplePhone", function(value, element) {
            return this.optional(element) || /^[0-9-+()\s]+$/.test(value);
        });

        $.validator.addMethod("inArray", function(value, element) {
            var arr = [];
            if ($(element).data("array")) arr = $(element).data("array");
            if ($(element).data("array-select")) arr = htmlToArray($($(element).data("array-select")));
            return $.inArray(value.toLowerCase(), arr) !== -1;
        });

        $.validator.methods.url = function(value, element, param) {
            return this.optional( element ) || /^(http|https):\/\//i.test( value );
        }

        $.validator.setDefaults({ ignore: 'input:not(.form-control--notignore):hidden' });

    }

    function fixAutofill(){
        setTimeout(function(){
            if ($(":-webkit-autofill").length)
                $(":-webkit-autofill").parents(".form-group.is-empty").removeClass("is-empty");
        }, 100)
    }

    function clearErrors(form, el){
        var id = form.attr("id");

        $(".alert:visible[data-form="+ id + "]").fadeOut(function(){
            $(this).remove();
        });

        if (el){
            el.parents(".form-group.has-error").removeClass("has-error");
            el.siblings("span.has-error").remove();
        }
    }

    return {
        init: function(){
            fixAutofill();
            initValidator();

            forms.each(function(){
                var form = $(this);

                // Hide alert and errors on change form
                form.find('.form-control').on('keyup', function(){
                    clearErrors(form, $(this));
                });

                form.find('[type=submit]').on('click', function(){
                    clearErrors(form);
                });
            });

            validateForms.each(function(){
                var form = $(this);
                var id=$(this).attr("id");

                //validate

                form.validate({
                    errorClass: "has-error",
                    errorElement:"span",
                    highlight: function(element, errorClass, validClass) {
                        element = $(element);
                        var elementParent =  element.parents(".form-group").length ? element.parents(".form-group") : element.parent();
                        if ( element[0].type === "radio" ) {
                            $(element).addClass( errorClass ).removeClass( validClass );
                        } else {
                            element.addClass( errorClass ).removeClass( validClass );
                            elementParent.addClass(errorClass);
                        }

                        // Highlight parent block instead error placement
                        if (element.is("[data-highlight]")){
                            var highlightedBlock = $($(element).data("highlight"));
                            highlightedBlock.addClass("error-highlight");
                        }
                    },
                    errorPlacement: function(error, element) {
                        if (!element.is("[data-noerror]")){
                            var elementParent =  element.parents(".form-group").length ? element.parents(".form-group") : element.parent();
                            elementParent.append(error);
                        }
                    },
                    unhighlight: function( element, errorClass, validClass ) {
                        element = $(element);
                        if ( element[0].type === "radio" ) {
                            $(element).removeClass( errorClass ).addClass( validClass );
                        } else {
                            element.removeClass( errorClass ).addClass( validClass );
                            element.parents("." + errorClass).removeClass(errorClass);
                        }

                        // Unhighlight parent block instead error placement
                        if (element.is("[data-highlight]")){
                            var highlightedBlock = $(element.data("highlight"));
                            highlightedBlock.removeClass("error-highlight");
                        }
                    }
                });
            })
        }
    }
})();

// Messages module
var Messages = (function(){
    return {
        init: function(){
            if ($(".alert--timeout").length){
                $(".alert--timeout").each(function(){
                    var alert=$(this);
                    setTimeout(function(){
                        alert.fadeOut(function(){
                            alert.remove();
                        });
                    }, 3000);
                })
            }
        }
    }
})();

// Dynamic fields
var DynamicFieds =(function(){
    var fields = $(".form-control--dynamic");

    function clearTarget(el){
        el.each(function(){
            $(this).find(".form-control").val("").change();
        })
    }

    return {
        init: function(){
            fields.each(function(){
                var me = $(this);
                var target = $(me.data("relative-field")).parents(".form-group").hide();

                me.on("keyup paste", function(){
                    if (me.val() != "")
                        target.each(function(){
                            $(this).slideDown()
                        })
                    else
                        target.each(function(){
                            $(this).slideUp(function(){
                                clearTarget($(this));
                            });
                        });
                })
            })
        }
    }
})();

// Service menu
var Nav = (function(){
    var menuLink = $(".js-service-menu"),
        menu = $(".nav__service-menu"),
        nav = $(".nav"),
        overlay = $(".overlay");

    function checkBordered(){
        if ($(window).scrollTop() < 100){
            if (!menu.is(":visible")) result.unborderedNav();
        } else
            result.borderedNav();
    }

    function scrollWatcher(){
        checkBordered();
        $(window).on("scroll", function(){
            checkBordered()
        });
    }

    var result =  {
        init: function(){
            scrollWatcher();

            if (menu.length){
                menuLink.on("click", function(){
                    if (menu.is(":visible"))
                        result.hideMenu()
                    else
                        result.showMenu();
                    return false;
                })

                overlay.on("click", function(){
                    result.hideMenu();
                })
            }
        },
        showMenu: function(){
            menu.slideDown(150, function(){
                result.borderedNav();
            });
            menuLink.addClass("shown");
            overlay.fadeIn(150);
        },
        hideMenu: function(){
            menu.slideUp(150, function(){
                checkBordered();
            });
            menuLink.removeClass("shown");
            overlay.fadeOut(150);
        },
        borderedNav: function(){
            nav.addClass("bordered");
        },
        unborderedNav: function(){
            nav.removeClass("bordered");
        }
    }

    return result;
})();

// Plans
var Plans =(function(){
    var paymentForm = $(".choosen-plan__payment"),
        plansModal = $(".plans-modal");
        plansAlertModal = $(".plans-alert-modal");

    function showResult(plan, paid, container){
        var slider = $(".choosen-plan__header." + plan).find(".slider")[0];
        $(".choosen-plan__header." + plan).addClass("active");
        if (paid) paymentForm.addClass("active");
        if (slider) slider.noUiSlider.set([slider.noUiSlider.get()]);
        container.addClass("choosen");
    }

    function hideResult(container){
        if (container.parents(".plans-modal").length)
            plansModal.removeClass("choosen");
        container.removeClass("choosen");
        $("#ngw_plans_period").val("1");
        setTimeout(function(){
            container.find(".choosen-plan__header.active").removeClass("active");
            paymentForm.removeClass("active");
        }, 600);
    }

    return {
        init: function(){
            var isInPopup = plansModal.length ? true : false;

            if (isInPopup)  {
                plansModal.modal();

                if (window.location.hash === "#plans" || get_query_value("show_plans")!= null){
                    plansModal.modal("show");
                }

                plansModal.on('shown.bs.modal', function (e) {
                    window.location.hash = "#plans"
                });

                plansModal.on('hidden.bs.modal', function (e) {
                    window.location.hash = ""
                    $(this).find(".js-plan-back").click();
                });

                $('.js-switch-customer-type').on('shown.bs.tab', function (e) {
                    if ($(e.target).data("target")=="#yridical") {
                        $(".choosen-plan__btn-text--pay").addClass("hidden");
                        $(".choosen-plan__btn-text--order").removeClass("hidden");
                    } else {
                        $(".choosen-plan__btn-text--pay").removeClass("hidden");
                        $(".choosen-plan__btn-text--order").addClass("hidden");
                    }
                });
            }

            $(".plan-choice").each(function(){
                var cont = $(this),
                    wrapper = cont.parents(".plan-choice-wrapper"),
                    btn = cont.find(".js-choose-plan"),
                    backLink = cont.find('.js-plan-back'),
                    planInput = wrapper.find(".js-ngw-plan");

                btn.on("click", function(e){
                    e.preventDefault();
                    showResult($(this).data("plan"), $(this).data("paid-plan"), cont);
                    if (isInPopup) plansModal.addClass("choosen");
                    planInput.val($(this).data("plan")).valid();
                })

                backLink.on("click", function(e){
                    e.preventDefault();
                    hideResult(cont);
                    if (isInPopup) plansModal.removeClass("choosen");
                    planInput.val("");
                })
            })

            if (get_query_value("payment-success")!= null){
                if (plansAlertModal) plansAlertModal.modal("show");
            }
        }
    }
})();

// Radiotab module
var Radiotab = (function(){
    var detachedPanels = {},
        container = $(".tab-content"); // TODO - rewrite for multiple container on one page

    function addPanel(key){
        container.append(detachedPanels[key]);
        delete detachedPanels[key];
    }

    function removeSiblingsPanel(el){
        var siblingTabs = el.parent(".radio").siblings().find("[data-toggle=radiotab]");

        siblingTabs.each(function(){
            if ($($(this).data("target")).length)
                detachedPanels[$(this).data("target")] = $($(this).data("target")).detach();
        });
    }

    return {
        init: function(){

            $("[data-toggle=radiotab]").on("click", function(){
                var targetId = $(this).data("target");

                if ($(this).data("removeOther")!=undefined){
                    if (targetId in detachedPanels){
                        addPanel(targetId)
                    }
                    removeSiblingsPanel($(this));
                } else {
                    if (detachedPanels.length){
                        for(var key in detachedPanel){
                            container.append(detachedPanels[key]);
                        }
                    }
                }
                $(this).tab("show");
            })

            $("[data-toggle=radiotab]").find(":checked").parents("[data-toggle=radiotab]").click();
        }
    }
})();

// Autocomplete module

var Autocomplete = (function(){
    var elements = $(".autocomplete");
    return {
        init: function(){
            elements.each(function(){
                el = $(this)[0];
                new autoComplete({
                    selector: el,
                    minChars: 0,
                    source: function(term, suggest){
                        term = term.toLowerCase();
                        var choices = [];
                        var matches = [];

                        if ($(el).data("array-select")) choices = htmlToArray($($(el).data("array-select")));

                        for (i=0; i<choices.length; i++)
                            if (~choices[i].toLowerCase().indexOf(term)) matches.push(choices[i]);
                        suggest(matches);
                    },
                    delay: 0
                });


                if ($(el).data("array-select")){
                    var select = $($(el).data("array-select"));
                    if (select.find("[selected]").length) elements.val(select.find("[selected]").text().toLowerCase());

                    $(el).on('focusout', function(e) {
                        var value = $(this).val().toLowerCase();
                        select.find("option")
                            .removeAttr("selected")
                            .each(function(){
                                if ($(this).text().toLowerCase() == value) {
                                    $(this).prop('selected', true);
                                }
                            })
                    });
                }
            })

            elements.on('keypress keydown keyup', function(e) {
                if (e.which == 13 || e.keyCode == 13) {
                    e.preventDefault();
                }
            });
        }
    }
})();

// Slider module

var Slider = (function(){
    var sliders = $(".slider");

    function calcPriceValue(value, discount, slider){
        var discount = discount ? discount : 0,
            priceValue = parseFloat(slider.data("price")),
            totalPriceTarget = $(slider.data("totalprice-target")),
            totalPriceWithotDiscountTarget = $(slider.data("totalprice-withoutdiscount-target")),
            total = value*priceValue + value*priceValue*discount,
            totalWithoutDiscount = value*priceValue;

        totalPriceTarget.html(parseFloat(total).format(0,3));
        if (discount != 0)
            totalPriceWithotDiscountTarget.html(parseFloat(totalWithoutDiscount).format(0,3)).parent().stop().slideDown(400);
        else
            totalPriceWithotDiscountTarget.parent().stop().slideUp(300);

        if (slider.data("totalprice-input"))
            $(slider.data("totalprice-input")).val(total);
        if (slider.data("pipdiscount-input"))
            $(slider.data("pipdiscount-input")).val(discount);
    }

    var me = {
        init: function(){
            sliders.each(function(){
                var slider = $(this),
                    firstUpdate =true,
                    sliderStart = slider.data("start") ? slider.data("start").toString().split(",").map(function(item) {
                        return parseFloat(item);
                    }) : undefined,
                    sliderRange = slider.data("range") ? slider.data("range").split(",").map(function(item) {
                        return parseFloat(item);
                    }) : undefined,
                    sliderStep = slider.data("step") ? parseFloat(slider.data("step")) : undefined,
                    pipValue = slider.data("pip-values") ? slider.data("pip-values").split(",").map(function(item) {
                        return parseInt(item);
                    }) : undefined,
                    pipDiscount = slider.data("pip-discount") ? slider.data("pip-discount").split(",").map(function(item) {
                        return item ? parseFloat(item):null;
                    }) : undefined,
                    pipDiscountValue = {};

                if (pipValue && pipDiscount)
                    pipValue.forEach(function(item, index){
                        pipDiscountValue[item] = pipDiscount[index];
                    });

                noUiSlider.create(slider[0], {
                    start: sliderStart ? sliderStart : 0,
                    range: sliderRange ? {
                        'min': [ sliderRange[0] ],
                        'max': [ sliderRange[1] ]
                    } : {
                        'min': [ 0 ],
                        'max': [ 100 ]
                    },
                    step: sliderStep ? sliderStep : undefined,
                    pips: {
                        mode: pipValue ? "values": "steps",
                        values: pipValue,
                        density: 9,
                        format:{
                            to: function(value){
                                return pipDiscountValue[value] ? value + "<span class='noUi-value-add'>" + pipDiscountValue[value]*100 + "%</span>" : value;
                            },
                            from: function(value){
                                return pipDiscountValue[value] ? value + "<span class='noUi-value-add'>" + pipDiscountValue[value]*100 + "%</span>" : value;
                            },
                        }
                    },
                    tooltips: [{
                        to: function(value){
                            return slider.data("tooltip-postfix") ? parseInt(value) + " " + slider.data("tooltip-postfix") : parseInt(value);
                        },
                        from: function(value){
                            return slider.data("tooltip-postfix") ? parseInt(value) + " " + slider.data("tooltip-postfix") : parseInt(value);
                        },
                    }],
                    format: {
                        to: function(value){return parseInt(value)},
                        from: function(value){return parseInt(value)},
                    }
                });


                slider[0].noUiSlider.on('update', function(values){
                    var value = values[0];
                    if (slider.data("input") && !firstUpdate)
                        $(slider.data("input")).val(value);

                    if (firstUpdate){
                        firstUpdate = false;
                        slider.find(".noUi-base").append(slider.find(".noUi-pips").detach());
                    }

                    if (slider.data("price") && slider.data("totalprice-target"))
                        calcPriceValue(value, pipDiscountValue[value], slider);
                });
            })
        }
    }

    if (sliders.length)
        me.init();

    return me;
})();

// Format
var Format = (function(){
    var dataToFormat = $("[class^='format-']");
    var me = {
        init: function(){
            dataToFormat.each(function(){
                value = parseFloat($(this).text().replace(" ", ""));
                $(this).text(value.format(0,3));
            })
        }
    }

    if (dataToFormat.length)
        me.init();

    return me;
})();

// Fix bootstrap padding-right for fixed navbar
function fixBootstrap(){
    $(window).load(function(){
        var oldSSB = $.fn.modal.Constructor.prototype.setScrollbar;
        $.fn.modal.Constructor.prototype.setScrollbar = function(){
            oldSSB.apply(this);
            if(this.bodyIsOverflowing && this.scrollbarWidth)
            {
                $('.header, .navbar-fixed-top, .navbar-fixed-bottom').css('right', this.scrollbarWidth);
            }
        }

        var oldRSB = $.fn.modal.Constructor.prototype.resetScrollbar;
        $.fn.modal.Constructor.prototype.resetScrollbar = function(){
            oldRSB.apply(this);
            $('.header, .navbar-fixed-top, .navbar-fixed-bottom').css('right', '');
        }
    });
}

// Extend bootstrap tabs
var Tabs = (function(){
    var tab = $("[data-nav-active] [data-toggle='tab']");
    var me = {
        init: function(){
            tab.each(function(){
                var item = $(this);
                var parent = item.parents("[data-nav-active]");
                item.on('show.bs.tab', function (e) {
                    parent.addClass(parent.data("nav-active"));
                })
            })
        }
    }

    if (tab.length)
        me.init();

    return me;
})();

// Show trigger
var ShowTrigger = (function(){
    var showTrigger = $("a[data-show]"),
        hideTrigger = $("a[data-hide]");

    var me = {
        init: function(){
            showTrigger.on("click", function(e){
                var target = $($(this).data("show"));
                e.preventDefault();
                if (target.length){
                    if ($(this).data("show-class"))
                        target.addClass("show-class");
                    target.addClass("show");
                }
            });

            hideTrigger.on("click", function(e){
                var target = $($(this).data("hide"));
                e.preventDefault();
                if (target.length){
                    if ($(this).data("hide-class"))
                        target.addClass("hide-class");
                    target.removeClass("show");
                }
            })
        }
    }

    if (showTrigger.length || hideTrigger.length)
        me.init();

    return me;
})();


// Inner form
var InnerForm = (function(){
    var innerForm = $(".inner-form");

    function updateControlsValue(el){
        el.each(function(){
           $(this).attr("data-inner-form-init", $(this).val());
        });
    }

    function updateRelated(form, parentForm){
        if (form.data("innerFormRelated")){
            var target = parentForm.find(form.data("innerFormRelated")),
                str = "";
            form.find("input, select").each(function(index){
                if ($(this).val()){
                    if (str!="") str += ", ";
                    str += $(this).val();
                }
            });
            target.html(str);
        }
    }

    var me = {
        init: function(){
            innerForm.each(function(){
                var form = $(this),
                    controls = form.find("input, textarea, select"),
                    saveBtn = form.find(".inner-form__save-btn"),
                    cancelBtn = form.find(".inner-form__cancel-btn");

                updateControlsValue(controls);
                updateRelated(form, form.parents("form"));

                saveBtn.on("click", function(e){
                    if (controls.valid()) {
                        updateControlsValue(controls);
                        updateRelated(form, form.parents("form"));
                        form.trigger("innerForm.save");
                        form.removeClass("show");
                    }
                    e.preventDefault();
                });

                cancelBtn.on("click", function(e){
                    controls.each(function(){
                        $(this).val($(this).attr("data-inner-form-init"));
                    });
                    form.removeClass("show");
                    e.preventDefault();
                });
            })
        }
    }

    if (innerForm.length)
        me.init();

    return me;
})();

// Select
var Select= (function(){
    var select = $(".select");
    var me = {
        init: function(){
            select.dropdown({
                callback: function ($dropdown) {
                    var dropdownCls = $dropdown.siblings("select").data("selectClass");
                    $dropdown.addClass(dropdownCls);
                }
            });
        }
    }

    if (select.length){
        me.init();
    }
    return me;
})();

// Select
var ImageSelect= (function(){
    var imageSelect = $(".image-select");

    function getSrc(val, template){
        val = val || "default";
        return template.replace("$val", val);
    }

    function setSelectedImg(input, src){
        input.css({
            backgroundImage: "url('" + src + "')"
        });
    }

    var me = {
        init: function(){
            imageSelect.each(function(){
                var control = $(this),
                    srcTemplate = control.data("imageSelectSrc"),
                    fakeInput;
                control.dropdown({
                    "dropdownClass":"image-select",
                    "callback": function ($dropdown) {
                        fakeInput = control.siblings(".dropdownjs").find("input");
                        if (imageSelect.attr("tabindex")) fakeInput.attr("tabindex", imageSelect.attr("tabindex"));
                        setSelectedImg(fakeInput, getSrc(control.val(), srcTemplate));

                        $dropdown.find("li").each(function () {
                            $(this).html("<img class='image-select__pic' width='100' src='" +
                                        getSrc($(this).attr("value"), srcTemplate) + "' " +
                                        "title = '" + $(this).text() + "'>");
                        });
                    }
                });

                control.on("change", function(){
                    setSelectedImg(fakeInput, getSrc($(this).val(), srcTemplate));
                });
            })
        }
    }

    if (imageSelect.length)
        me.init();
    return me;
})();

var Scrollto = (function(){
    var me = {
        init: function(){
             $('.scrollto-link').on('click', function(e){
                var target=$(this).attr('href');
                me.scrollTo(target);
                e.preventDefault();
            })
        },
        scrollTo: function(target){
            if ($(target).length){
                $('html, body').animate({'scrollTop':$(target).offset().top - $(".header").outerHeight()},500);
            }
        }
    }
    if ($(".scrollto-link").length) me.init();

    if (window.location.hash){
        setTimeout(function(){
            me.scrollTo($(window.location.hash));
        }, 1);
    }
    return me;
})();

$(document).ready(function(){
    $.material.options = {
      "input": true,
      "ripples": true,
      "checkbox": true,
      "togglebutton": true,
      "radio": true,
      "arrive": true,
      "autofill": true,

      "withRipples": [
        ".btn:not(.withoutripple)",
        ".card-image",
        ".navbar a:not(.withoutripple)",
        ".dropdown-menu a",
        ".nav-tabs a:not(.withoutripple)",
        ".withripple",
        ".pagination li:not(.active):not(.disabled) a:not(.withoutripple)"
      ].join(","),
      "inputElements": "input.form-control, textarea.form-control",
      "checkboxElements": ".checkbox > label > input[type=checkbox], label.checkbox-inline > input[type=checkbox]",
      "togglebuttonElements": ".togglebutton > label > input[type=checkbox]",
      "radioElements": ".radio > label > input[type=radio], label.radio-inline > input[type=radio]"
    }
    svg4everybody();
    $.material.init();

    fixBootstrap();

    // Fixed nav
    if ($(".nav--fixed").length){
        Nav.init();
    }

    // Athorization and registration panel
    if ($(".auth-panel").length){
        AuthPanel.init();
        $(".js-authPanel").on("click", function(e){
            var target=$(this).attr("href");
            if (target) AuthPanel.show(target);
            e.preventDefault();
        });
    }

    // Forms
    if ($("form").length)
        Forms.init();

    // Messages
    if ($(".alert").length)
        Messages.init();

    //Dynamic fields
    if ($(".form-control--dynamic").length)
        DynamicFieds.init();

    //Plans
    if ($(".plan-choice, .plans-modal").length)
        Plans.init();

    //error report
    if ($("#error-report-link").length){
        $("#error-report-link").prop("href" , $("#error-report-link").prop("href") + " " + window.location.href);
    }

    // Radio tab
    if ($("[data-toggle=radiotab]").length){
        Radiotab.init();
    }

    // Autocomplete
    if ($(".autocomplete").length){
        Autocomplete.init();
    }

    $("select").change();
});
