<template>
  <div class="ng-collapsible" :class = "{ collapsed: isCollapsed, activatorAsLink: activatorAsLink }">
    <div class="ng-collapsible__activator" @click = "toggleContent">
      <template v-if="activatorAsLink">
        <a class="ng-collapsible__activator-content fake-link" href="#" @click.prevent>
          <slot name="activator"></slot>
        </a>
      </template>
      <template v-else>
        <span class="ng-collapsible__activator-content">
          <slot name="activator"></slot>
        </span>
      </template>
      <v-icon class="ng-collapsible__activator-icon" v-if="withIcon" >arrow_drop_up</v-icon>
    </div>
    <v-expand-transition>
      <div class="ng-collapsible__content" v-show = "!isCollapsed">
        <slot name="content"></slot>
      </div>
    </v-expand-transition>
  </div>
</template>

<script>

  export default {

    name: 'NgCollapsible',
    props: {
      collapsed: {
        type: Boolean,
        default: true
      },
      withIcon: {
        type: Boolean,
        default: true
      },
      activatorAsLink: {
        type: Boolean,
        default: false
      }
    },
    data () {
      return {
        isCollapsed: this.collapsed
      }
    },
    methods: {
      toggleContent() {
        this.isCollapsed = !this.isCollapsed;
      }
    }
  }
</script>

<style lang="styl" scoped>
  @require "~@nextgis_common/styl/variables/_variables";

  .ng-collapsible
    &__activator
      display: inline-block;
      cursor: pointer
      user-select: none;

    &__activator-content
      vertical-align: middle;

    &__activator-icon,
    &__activator-icon.v-icon
      transform: rotate(0deg);
      transition: transform .3s;
      vertical-align: middle;

    &.collapsed
      .ng-collapsible__activator-icon
        transform: rotate(-180deg);

    &.activatorAsLink

      .ng-collapsible__activator-icon,
      .ng-collapsible__activator-icon.v-icon
        color: $link-color;

      .ng-collapsible__activator:hover
          .ng-collapsible__activator-icon,
          .ng-collapsible__activator-content
            color: $link-hover-color;
</style>
