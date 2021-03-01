<template>
  <v-app v-cloak :class="[
    'ng-layout',
    'ng-sidebar-layout',
    {'ng-sidebar-layout--fluid': fluid}
  ]">
    <slot name="header">
      <app-header
        :service-name = "_config.serviceName"
        :menu-items = "_config.topMenuItems"
        :active-menu-item = "currentPage"
        @menu-icon-click = "sidebarMenuShown = true"
        :fluid = "fluid">
      </app-header>
    </slot>

    <v-main class="main">
      <v-container class="main__container" :class="contentBg"
        pa-0
        :fluid="fluid">
        <div class="ng-layout-sidebar">
          <v-navigation-drawer
            class="ng-layout-sidebar__sidebar app-sidebar app-sidebar--content"
            width="200" height="auto"
            v-model="sidebarMenuShown" floating
          > <!-- TODO move to AppSidebar.vue -->
            <slot name="sidebar">
              <app-menu
                :items="_config.topMenuItems"
                :active-item="currentPage"
                view="vertical">
              </app-menu>
            </slot>
          </v-navigation-drawer>
          <div class="ng-layout-sidebar__content">
            <div class="main__content">
              <v-container pa-0 :fluid="!contentCentered">
                <slot></slot>
              </v-container>
            </div>
          </div>
        </div>
      </v-container>
    </v-main>

    <slot name="footer">
      <app-footer dark :fluid="fluid" centered
        :view="_config.footerView || 'small'"
        :menu-items="_config.bottomMenuItems">
      </app-footer>
    </slot>
  </v-app>
</template>

<script>
import AppHeader from '@nextgis_common/components/AppHeader/AppHeader.vue';
import AppFooter from '@nextgis_common/components/AppFooter/AppFooter.vue';
import AppMenu from '@nextgis_common/components/AppMenu/AppMenu.vue';

import { mapState } from 'vuex';

export default {

  name: 'SidebarLayout',
  components: {
    AppHeader,
    AppFooter,
    AppMenu
  },
  props: {
    fluid: {
      type: Boolean,
      default: false
    },
    contentBg: {
      type: String,
      default: 'white'
    },
    contentCentered:{
      type: Boolean,
      default: false
    },
    config: {
      type: Object,
      default: null
    }
  },

  data() {
    return {
      sidebarMenuShown: false
    };
  },
  computed:{
    ...mapState(['baseApp']),
    _config(){
      return this.config || this.baseApp.config;
    },
    currentPage(){
      return this.baseApp ? this.baseApp.currentPage.id : null
    }
  }
};
</script>

<style lang="scss" scoped>
  .ng-sidebar-layout{
    &::v-deep .main{
      background-color: transparent;
    }
  }

  .ng-layout-sidebar{
    width: 100%;

    &__content{
      transition: margin-left 0.6s cubic-bezier(0.4, 0, 0.2, 1);
      margin-left: 0;

      @media (min-width: $mobile-breakpoint){
        margin-left: 200px;
      }
    }
  }
</style>
