<template>
  <header class="header">
    <v-container class="header__container-1" pa-0 :fluid="fluid">
      <v-container class="header__container-2" py-0 :fluid="!centered">
        <div class="header__logo">
          <v-icon class="header__menu-btn header__menu-btn--temporary-sidebar"
            @click="$emit('menu-icon-click')"
            >
            menu
          </v-icon>
          <a href="/" class="withoutripple">
            <app-logo></app-logo>
          </a>
        </div>

        <div class="header__title h1">
          <a href="/">{{ serviceName }}</a>
        </div>

        <nav class="header-menu hidden-sm-and-down" >
          <slot name="header-menu">
            <app-menu
              :items="menuItems"
              :active-item="baseApp.currentPage.id">
            </app-menu>
          </slot>
        </nav>

        <v-spacer></v-spacer>

        <div class="header__right">
          <slot name="action">
          </slot>

          <template v-if="withAuthorization">
            <slot name="user">

              <template v-if="baseUser.IsAuthenticated">
                 <!--  TODO user component with current plan-->
              </template>

              <template v-else>
                <ng-button text class="ml-1" color="primary"
                  href="#">
                  Sign in
                </ng-button>
              </template>

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
    fluid: {
      type: Boolean,
      default: false
    },
    centered: {
      type: Boolean,
      default: false
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
    margin:0;
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

    &--content-sidebar {
      @media (min-width: $sidebar-breakpoint) {
        display: none !important;
      }
    }

    &--temporary-sidebar {
      @media (min-width: map-get($grid-breakpoints, 'md')) {
        display: none !important;
      }
    }


    & + .header__logo .logo--mini{
      margin-right: 2px;
    }
  }
}

.header__right{
  margin-right: -8px;
}

.header__logo{
  position: relative;
  padding-right: 16px;
  margin-right: 14px;

  &:after{
    content:"";
    position: absolute;
    right:0;
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
}
</style>
