<template>
  <div :class="[
    'ng-layout',
    'ng-base-layout',
    {'ng-base-layout--fluid': fluid}
  ]">
    <slot name="header">
      <app-header
        :service-name = "config.serviceName"
        :menu-items = "config.topMenuItems"
        :with-authorization = "config.withAuthorization"
        @menu-icon-click = "sidebarMenuShown = true"
        :fluid = "fluid">
      </app-header>
    </slot>

    <v-main class="main">
      <v-container class="main__container" :class="contentBg"
        pa-0
        :fluid="fluid">
        <div class="layout-nosidebar">
          <div class="main__content">
            <v-container pa-0 :fluid="!contentCentered">
              <slot></slot>
            </v-container>
          </div>
        </div>
      </v-container>
    </v-main>

    <v-navigation-drawer
      class="app-sidebar app-sidebar--temporary" temporary fixed
      width="200" height="auto"
      v-model="sidebarMenuShown" floating
    > <!-- TODO move to AppSidebar.vue -->
      <slot name="sidebar">
        <app-menu
          :items="config.topMenuItems"
          :active-item="baseApp.currentPage.id"
          view="vertical">
        </app-menu>
      </slot>
    </v-navigation-drawer>

    <slot name="footer">
      <app-footer dark :fluid="fluid" centered
        :view="config.footerView || 'small'"
        :menu-items="config.bottomMenuItems">
      </app-footer>
    </slot>
  </div>
</template>

<script>
import AppHeader from '@nextgis_common/components/AppHeader/AppHeader.vue';
import AppFooter from '@nextgis_common/components/AppFooter/AppFooter.vue';
import AppMenu from '@nextgis_common/components/AppMenu/AppMenu.vue';

import { mapState } from 'vuex';

export default {

  name: 'BaseLayout',
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
    }
  },
  data() {
    return {
      sidebarMenuShown: false
    };
  },
  computed:{
    ...mapState(['baseApp']),
    config(){
      return this.baseApp.config;
    }
  }
};
</script>

<style lang="scss" scoped>
  .ng-base-layout{
    &::v-deep .main{
      background-color: transparent;
    }
  }

  .layout-nosidebar{
    width: 100%;
  }
</style>
