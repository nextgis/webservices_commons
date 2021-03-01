<template>
  <header :class="[
    'header',
    {'header--dark': dark}
  ]">
    <v-container class="header__container-1" pa-0 :fluid="fluid">
      <v-container class="header__container-2" py-0 :fluid="!centered">
        <div class="header__logo">
          <v-icon class="header__menu-btn"
            @click="$emit('menu-icon-click')"
            >mdi-menu
          </v-icon>
          <slot name="logo">
            <a href="/" class="withoutripple">
              <app-logo :small = "logoView === 'small'"></app-logo>
            </a>
          </slot>
        </div>
        <slot name="title">
          <div class="header__title h1">
            <a href="/">{{ serviceName }}</a>
          </div>
        </slot>

        <nav class="header-menu" >
          <slot name="header-menu">
            <app-menu
              :items="menuItems"
              :active-item="activeMenuItem">
            </app-menu>
          </slot>
        </nav>

        <v-spacer></v-spacer>

        <div class="header__right">
          <slot name="action">
          </slot>

          <template v-if="withAuthorization">
            <slot name="user">

              <!-- <template v-if="userIsAuthenticated">
                   TODO user component with current plan
              </template> -->

              <!-- <template v-else> -->
                <ng-button text class="ml-1" color="primary"
                  href="#">
                  Sign in
                </ng-button>
              <!-- </template> -->

            </slot>
          </template>
        </div> <!--/header__right -->
      </v-container>
    </v-container>
  </header>
</template>

<script>
import { mapState } from 'vuex';
import { getUrl } from '@nextgis_common/services/UrlService';
import AppLogo from '@nextgis_common/components/AppLogo/AppLogo';
import AppMenu from '@nextgis_common/components/AppMenu/AppMenu';

export default {
  name: 'AppHeader',
  props: {
    dark: {
      type: Boolean,
      default: false
    },
    withAuthorization: {
      type: Boolean,
      default: true
    },
    serviceName: {
      type: String,
      default: ''
    },
    menuItems: {
      type: Array,
      default: []
    },
    activeMenuItem: {
      type: String
    },
    fluid: {
      type: Boolean,
      default: false
    },
    centered: {
      type: Boolean,
      default: false
    },
    logoView: {
      type: String,
      default: 'normal' // 'small'
    }
  },
  components: { AppLogo, AppMenu },
  data() {
    return {

    };
  },
  computed: {
    ...mapState(['baseApp','baseUser']),
    loginUrl(){
      return getUrl('ngid_login');
    }
  }
};
</script>

<style lang="scss" scoped>

.header{
  position: fixed;
  left: 0;
  right:0;
  top:0;
  height:$header-height-sm;
  min-height: $header-height-sm;
  z-index: 40;
  white-space: nowrap;
  backface-visibility: hidden;
  font-weight: 400;
  color: $text-base;
  font-size: 14px;
  width: 100%;

  @media (min-width: map-get($grid-breakpoints, 'sm')){
    height:$header-height;
  }

  &__container-1,
  &__container-2 {
    display: flex;
    align-items: center;
    height: 100%;
  }

  &__container-1{
    background-color: $ng-light-blue;
    border-bottom: 1px solid #d3e3f2;
  }

  h1, .h1{
    display: inline-block;
    font-size: map-get($font-size, 'base');
    margin-bottom:0;
    margin-top: 0;
    color: var(--v-primary-base);
    font-weight: 500;

    a,
    a:hover,
    a:focus,
    a:active{
      color: var(--v-primary-base);
    }
  }

  a{
    border-bottom: 0;
    text-decoration: none;
  }

  .btn{
    padding-left: 14px;
    padding-right: 14px;
  }

  .circle-btn{
    width:30px;
    height: 30px;
    border-radius: 50%;
    line-height: 30px;
    padding:0;
  }

  &__menu-btn{
    margin-left: -6px;
    margin-right: 6px;

    &.theme--light.v-icon {
      font-size: 24px;
      color: $dark-blue;
      vertical-align: middle;
    }

    @media (min-width: $mobile-breakpoint) {
      display: none !important;
    }

    & + .header__logo .logo--mini{
      margin-right: 2px;
    }
  }
}

.header__right{
  margin-right: -8px;
}

.header__title{
  position: relative;
  padding-left: 14px;
  margin-left: 14px;

  &:before{
    content:"";
    position: absolute;
    left:0;
    top: 0px;
    bottom: 0px;
    width: 2px;
    background-color: #b4d0ea;
  }
}

.header__plan{
  margin-left: 8px;

  @media (min-width: map-get($grid-breakpoints, 'sm')){
    margin-left: 12px;
  }
}

.header__user{
  display: inline-block;
  margin-left: 12px;

  &::not(:last-child){
    margin-right:12px;
  }
}

.header-menu{
  display: flex;
  margin-left: 38px;
  vertical-align: top;
  align-self: stretch;

  @media (max-width: $mobile-breakpoint){
    display: none;
  }
}

.header--dark{
  .header__container-1{
    background-color: $ng-primary-dark;
    border-bottom-color: $ng-primary-dark;
  }

  a, h1, .h1,
  h1 a , .h1 a{
    &,
    &:hover,
    &:focus,
    &:active{
      color: rgba(255,255,255,.92);
    }
  }

  &::v-deep .logo-pic,
  &::v-deep .logo-pic:hover{
    .logo-pic__item--light{
      fill: rgba(255,255,255,.92);
    }
    .logo-pic__item--dark{
    fill: $dark-blue;;
    }
  }
}
</style>
