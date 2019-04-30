import Bootstrap from 'bootstrap'
import BootstrapMD from 'bootstrap-material-design/dist/js/material'
import Ripples from 'bootstrap-material-design/dist/js/ripples'
import DropdownJS from 'dropdown.js'
import svg4everybody from 'svg4everybody'
import * as Util from './utilities'

export default function() {
  // Detect Ie
  var detectIe = (function () {
    var ie = 0;
    try { ie = navigator.userAgent.match(/(MSIE |Trident.*rv[ :])([0-9]+)/)[2]; }
    catch (e) {}
    if (ie !== 0) document.getElementsByTagName("html")[0].className += " ie v" + ie;
  })();

  Number.prototype.format = function (n, x) {
    var re = '\\d(?=(\\d{' + (x || 3) + '})+' + (n > 0 ? '\\.' : '$') + ')';
    return this.toFixed(Math.max(0, ~~n)).replace(new RegExp(re, 'g'), '$& ');
  };

  // Forms module
  var Forms = (function () {
    var forms = $("form");
    var validateForms = $(".form-validate");

    function initValidator () {
      validator();

      $.extend($.validator.messages, {
          required: validator_messages.required,
          email: validator_messages.email,
          url: validator_messages.url,
          date: validator_messages.date,
          number: validator_messages.number,
          creditcard: validator_messages.creditcard,
          equal: validator_messages.equal,
          userName : validator_messages.userName,
          personName : validator_messages.personName,
          domenName: validator_messages.domenName,
          simplePhone: validator_messages.simplePhone,
          inArray: validator_messages.inArray
      });

      $.validator.addMethod("equal", function (value, element) {
        var equalTo = $($(element).data("equalto"));
        if (equalTo.not(".validate-equalTo-blur").length) {
          equalTo.addClass("validate-equalTo-blur").on("blur.validate-equalTo", function () {
            $(element).valqualToid();
          });
        }
        return value === equalTo.val();
      });

      $.validator.addMethod("email", function (value, element) {
        return this.optional(element) || /^[a-zA-Z0-9.!#$%&'*+\/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)+$/.test(value);
      });

      $.validator.addMethod("userName", function (value, element) {
        return this.optional(element) || /^[a-zA-Z0-9-_/.]+$/.test(value);
      });

      $.validator.addMethod("domenName", function (value, element) {
        return this.optional(element) || /^[a-zA-Z][a-zA-Z0-9-]{2,61}[a-zA-Z0-9]$/.test(value);
      });

      $.validator.addMethod("personName", function (value, element) {
        return this.optional(element) || /^[^0-9-_+=\~!@#$%\^\&\*\,\.\?\|\\\/\"\№\;\:\(\)\<\>\{\}\[\]]+$/.test(value);
      });

      $.validator.addMethod("simplePhone", function (value, element) {
        return this.optional(element) || /^[0-9-+()\s]+$/.test(value);
      });

      $.validator.addMethod("inArray", function (value, element) {
        var arr = [];
        if ($(element).data("array")) arr = $(element).data("array");
        if ($(element).data("array-select")) arr = Util.htmlToArray($($(element).data("array-select")));
        return $.inArray(value.toLowerCase(), arr) !== -1;
      });

      $.validator.methods.url = function (value, element, param) {
        return this.optional(element) || /^(http|https):\/\//i.test(value);
      }

      $.validator.setDefaults({ignore: 'input:not(.form-control--notignore):hidden'});

    }

    function fixAutofill () {
      setTimeout(function () {
        try {
          if ($(":-webkit-autofill").length)
            $(":-webkit-autofill").parents(".form-group.is-empty").removeClass("is-empty");
        } catch {};
      }, 100)
    }

    function clearErrors (form, el) {
      var id = form.attr("id");

      $(".alert:visible[data-form=" + id + "]").fadeOut(function () {
        $(this).remove();
      });

      if (el) {
        el.parents(".form-group.has-error").removeClass("has-error");
        el.siblings("span.has-error").remove();
      }
    }

    return {
      init: function () {
        fixAutofill();
        initValidator();

        forms.each(function () {
          var form = $(this);

          // Hide alert and errors on change form
          form.find('.form-control').on('keyup', function () {
            clearErrors(form, $(this));
          });

          form.find('[type=submit]').on('click', function () {
            clearErrors(form);
          });
        });

        validateForms.each(function () {
          var form = $(this);
          var id = $(this).attr("id");

          //validate

          form.validate({
            errorClass: "has-error",
            errorElement: "span",
            highlight: function (element, errorClass, validClass) {
              element = $(element);
              var elementParent = element.parents(".form-group").length ? element.parents(".form-group") : element.parent();
              if (element[0].type === "radio") {
                $(element).addClass(errorClass).removeClass(validClass);
              } else {
                element.addClass(errorClass).removeClass(validClass);
                elementParent.addClass(errorClass);
              }

              // Highlight parent block instead error placement
              if (element.is("[data-highlight]")) {
                var highlightedBlock = $($(element).data("highlight"));
                highlightedBlock.addClass("error-highlight");
              }
            },
            errorPlacement: function (error, element) {
              if (!element.is("[data-noerror]")) {
                var elementParent = element.parents(".form-group").length ? element.parents(".form-group") : element.parent();
                elementParent.append(error);
              }
            },
            unhighlight: function (element, errorClass, validClass) {
              element = $(element);
              if (element[0].type === "radio") {
                $(element).removeClass(errorClass).addClass(validClass);
              } else {
                element.removeClass(errorClass).addClass(validClass);
                element.parents("." + errorClass).removeClass(errorClass);
              }

              // Unhighlight parent block instead error placement
              if (element.is("[data-highlight]")) {
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
  var Messages = (function () {
    return {
      init: function () {
        if ($(".alert--timeout").length) {
          $(".alert--timeout").each(function () {
            var alert = $(this);
            setTimeout(function () {
              alert.fadeOut(function () {
                alert.remove();
              });
            }, 3000);
          })
        }
      }
    }
  })();

  // Dynamic fields
  var DynamicFieds = (function () {
    var fields = $(".form-control--dynamic");

    function clearTarget (el) {
      el.each(function () {
        $(this).find(".form-control").val("").change();
      })
    }

    return {
      init: function () {
        fields.each(function () {
          var me = $(this);
          var target = $(me.data("relative-field")).parents(".form-group").hide();

          me.on("keyup paste", function () {
            if (me.val() != "")
              target.each(function () {
                $(this).slideDown()
              })
            else
              target.each(function () {
                $(this).slideUp(function () {
                  clearTarget($(this));
                });
              });
          })
        })
      }
    }
  })();

  // Radiotab module
  var Radiotab = (function () {
    var detachedPanels = {},
      container = $(".tab-content"); // TODO - rewrite for multiple container on one page

    function addPanel (key) {
      container.append(detachedPanels[key]);
      delete detachedPanels[key];
    }

    function removeSiblingsPanel (el) {
      var siblingTabs = el.parent(".radio").siblings().find("[data-toggle=radiotab]");

      siblingTabs.each(function () {
        if ($($(this).data("target")).length)
          detachedPanels[$(this).data("target")] = $($(this).data("target")).detach();
      });
    }

    return {
      init: function () {

        $("[data-toggle=radiotab]").on("click", function () {
          var targetId = $(this).data("target");

          if ($(this).data("removeOther") != undefined) {
            if (targetId in detachedPanels) {
              addPanel(targetId)
            }
            removeSiblingsPanel($(this));
          } else {
            if (detachedPanels.length) {
              for (var key in detachedPanel) {
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

  // Format
  var Format = (function () {
    var dataToFormat = $("[class^='format-']");
    var me = {
      init: function () {
        dataToFormat.each(function () {
          var value = parseFloat($(this).text().replace(" ", ""));
          $(this).text(value.format(0, 3));
        })
      }
    }

    if (dataToFormat.length)
      me.init();

    return me;
  })();

  // Fix bootstrap padding-right for fixed navbar
  function fixBootstrap () {
    $(window).on('load', function () {
      var oldSSB = $.fn.modal.Constructor.prototype.setScrollbar;
      $.fn.modal.Constructor.prototype.setScrollbar = function () {
        oldSSB.apply(this);
        if (this.bodyIsOverflowing && this.scrollbarWidth) {
          $('.header, .navbar-fixed-top, .navbar-fixed-bottom').css('right', this.scrollbarWidth);
        }
      }

      var oldRSB = $.fn.modal.Constructor.prototype.resetScrollbar;
      $.fn.modal.Constructor.prototype.resetScrollbar = function () {
        oldRSB.apply(this);
        $('.header, .navbar-fixed-top, .navbar-fixed-bottom').css('right', '');
      }
    });
  }

  // Extend bootstrap tabs
  var Tabs = (function () {
    var tab = $("[data-nav-active] [data-toggle='tab']");
    var me = {
      init: function () {
        tab.each(function () {
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
  var ShowTrigger = (function () {
    var showTrigger = $("a[data-show]"),
      hideTrigger = $("a[data-hide]");

    var me = {
      init: function () {
        showTrigger.on("click", function (e) {
          var target = $($(this).data("show"));
          e.preventDefault();
          if (target.length) {
            if ($(this).data("show-class"))
              target.addClass("show-class");
            target.addClass("show");
          }
        });

        hideTrigger.on("click", function (e) {
          var target = $($(this).data("hide"));
          e.preventDefault();
          if (target.length) {
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
  var InnerForm = (function () {
    var innerForm = $(".inner-form");

    function updateControlsValue (el) {
      el.each(function () {
        $(this).attr("data-inner-form-init", $(this).val());
      });
    }

    function updateRelated (form, parentForm) {
      if (form.data("innerFormRelated")) {
        var target = parentForm.find(form.data("innerFormRelated")),
          str = "";
        form.find("input, select").each(function (index) {
          if ($(this).val()) {
            if (str != "") str += ", ";
            str += $(this).val();
          }
        });
        target.html(str);
      }
    }

    var me = {
      init: function () {
        innerForm.each(function () {
          var form = $(this),
            controls = form.find("input, textarea, select"),
            saveBtn = form.find(".inner-form__save-btn"),
            cancelBtn = form.find(".inner-form__cancel-btn");

          updateControlsValue(controls);
          updateRelated(form, form.parents("form"));

          saveBtn.on("click", function (e) {
            if (controls.valid()) {
              updateControlsValue(controls);
              updateRelated(form, form.parents("form"));
              form.trigger("innerForm.save");
              form.removeClass("show");
            }
            e.preventDefault();
          });

          cancelBtn.on("click", function (e) {
            controls.each(function () {
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
  var Select = (function () {
    var select = $(".select");
    var me = {
      init: function () {
        select.dropdown({
          callback: function ($dropdown) {
            var dropdownCls = $dropdown.siblings("select").data("selectClass");
            $dropdown.addClass(dropdownCls);
          }
        });
      }
    }

    if (select.length) {
      me.init();
    }
    return me;
  })();

  // Select
  var ImageSelect = (function () {
    var imageSelect = $(".image-select");

    function getSrc (val, template) {
      val = val || "default";
      return template.replace("$val", val);
    }

    function setSelectedImg (input, src) {
      input.css({
        backgroundImage: "url('" + src + "')"
      });
    }

    var me = {
      init: function () {
        imageSelect.each(function () {
          var control = $(this),
            srcTemplate = control.data("imageSelectSrc"),
            fakeInput;
          control.dropdown({
            "dropdownClass": "image-select",
            "callback": function ($dropdown) {
              fakeInput = control.siblings(".dropdownjs").find("input");
              if (imageSelect.attr("tabindex")) fakeInput.attr("tabindex", imageSelect.attr("tabindex"));
              setSelectedImg(fakeInput, getSrc(control.val(), srcTemplate));

              $dropdown.find("li").each(function (index) {
                var value = control.find("option:eq(" + index + ")").val();
                $(this).html("<img class='image-select__pic' width='100' src='" +
                  getSrc(value, srcTemplate) + "' " +
                  "title = '" + $(this).text() + "'>");
              });
            }
          });

          control.on("change", function () {
            setSelectedImg(fakeInput, getSrc($(this).val(), srcTemplate));
          });
        })
      }
    }

    if (imageSelect.length)
      me.init();
    return me;
  })();

  var Scrollto = (function () {
    var me = {
      init: function () {
        $('.scrollto-link').on('click', function (e) {
          var target = $(this).attr('href');
          me.scrollTo(target);
          e.preventDefault();
        })
      },
      scrollTo: function (target) {
        if ($(target).length) {
          $('html, body').animate({'scrollTop': $(target).offset().top - $(".header").outerHeight()}, 500);
        }
      }
    }
    if ($(".scrollto-link").length) me.init();

    if (window.location.hash) {
      setTimeout(function () {
        me.scrollTo($(window.location.hash));
      }, 1);
    }
    return me;
  })();

  $(document).ready(function () {
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

    // Forms
    if ($("form").length)
      Forms.init();

    // Messages
    if ($(".alert").length)
      Messages.init();

    //Dynamic fields
    if ($(".form-control--dynamic").length)
      DynamicFieds.init();

    //error report
    if ($("#error-report-link").length) {
      $("#error-report-link").prop("href", $("#error-report-link").prop("href") + " " + window.location.href);
    }

    // Radio tab
    if ($("[data-toggle=radiotab]").length) {
      Radiotab.init();
    }

    $("select").change();
  });
}
