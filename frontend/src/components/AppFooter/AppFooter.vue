<template>
  <footer class="footer"
    :class="[
      `footer--${view}`,
      {
      'footer--dark': dark
      }
    ]">
    <v-container class="footer__container-1" pa-0 :fluid="fluid">
      <v-container class="footer__container-2" py-0 :fluid="!centered">

        <template v-if="view === 'large'">

          <div class="footer__left">
            <slot name="left">
              <footer-menu class="hidden-sm-and-down"
                :items="footerMenuItems"></footer-menu>
              <div class="footer__copyright">
                © {{ currentYear }} <a :href="nextgisSiteUrl" target="_blank">NextGIS</a>
                <a class="ml-4" :href="`maito:{$email}`">{{ email }}</a>
              </div>
            </slot>
          </div>
          <v-spacer></v-spacer>
          <div class="footer__right">
            <slot name="right">
              <locale-switcher class="footer__locale-switcher"></locale-switcher>
            </slot>
          </div>
        </template>

        <template v-else>
          <div class="footer__left">
            <slot name="left">
              <div class="footer__copyright">
                © {{ currentYear }} <a :href="nextgisSiteUrl" target="_blank">NextGIS</a>
                <a class="ml-4" :href="`maito:{$email}`">{{ email }}</a>
              </div>
            </slot>
          </div>
          <v-spacer></v-spacer>
          <div class="footer__right">
            <slot name="right">
              <footer-menu class="hidden-sm-and-down"
                :items="footerMenuItems"></footer-menu>
            </slot>
          </div>
        </template>
      </v-container>
    </v-container>
  </footer>
</template>

<script>
import { getUrlByLocale } from '@nextgis_common/services/UrlService';
import FooterMenu from '@nextgis_common/components/FooterMenu/FooterMenu';
import LocaleSwitcher from '@nextgis_common/components/LocaleSwitcher/LocaleSwitcher';

export default {

  name: 'AppFooter',
  components: { FooterMenu, LocaleSwitcher },
  i18n: {
    messages: {
      en: {
        message: {
          terms: "Terms of Service",
          privacy: "Privacy Policy",
        }
      },
      ru: {
        message: {
          terms: "Пользовательское соглашение",
          privacy: "Политика конфиденциальности",
        }
      }
    }
  },
  props: {
    view: {
      type: String, // small, large
      default: 'small'
    },
    dark: {
      type: Boolean,
      default: false
    },
    fluid: {
      type: Boolean,
      default: false
    },
    centered: {
      type: Boolean,
      default: false
    },
    menuItems: {
      type: Array,
      default: null
    },
    email: {
      type: String,
      default: 'info@nextgis.com'
    }
  },
  data() {
    return {
    };
  },
  computed: {
    currentYear() {
      return new Date().getFullYear();
    },
    nextgisSiteUrl() {
      return getUrlByLocale('nextgis_site', this.$i18n.locale);
    },
    footerMenuItems() {
      return this.menuItems || [
        {
          text: this.$t('message.terms'),
          link: `${this.nextgisSiteUrl}/terms`
        },
        {
          text: this.$t('message.privacy'),
          link: `${this.nextgisSiteUrl}/privacy`
        }
      ]
    }
  }
};
</script>

<style lang="scss" scoped>
.footer,
.v-application .footer{
  display: flex;
  position: relative;
  height:$footer-height;
  font-size: 13px;
  z-index: 10;
  flex-basis: auto;
  align-items: center;
  flex-shrink: 0;
  flex-grow: 0;
  padding-top: 0;
  padding-bottom: 0;

  &::v-deep a{
    color: #9e9e9e;
    text-decoration: none;
    border-bottom: 1px solid rgba(153, 151, 156,.24);

    &:hover,
    &:active,
    &:focus{
      border-bottom:0;
      color: var(--v-primary-base);
    }
  }

  &__container-1,
  &__container-2{
    display: flex;
    height: 100%;
    align-items: center;
  }

  &__container-1{
    background-color: #fff;
    color:$light-textColor;
  }

  &__locale-switcher{
    &::v-deep .locale-switcher__icon{
      font-size: 18px;
      color: rgba(255,255,255,.4);
      line-height: 15px;
    }
  }

  &--dark{
    &::v-deep .footer__container-1{
      background-color: #2d2d2d;
      color: rgba(255,255,255,.4);
    }

    &::v-deep a{
      color: rgba(255,255,255,.4);

      &:hover,
      &:active,
      &:focus{
        color: #fff;
      }
    }
  }

  &.footer--large{
    height: 224px;
    align-items:flex-start;

    &::v-deep .footer__container-2{
      padding-top:56px !important;
      padding-bottom: 56px !important;
    }

    &::v-deep .footer-menu{
      margin: 0 0 8px;
    }
    &::v-deep .footer-menu__item{
        display: inline-block;
        margin-right: 16px;
        margin-left: 0;
    }
  }
}

</style>

