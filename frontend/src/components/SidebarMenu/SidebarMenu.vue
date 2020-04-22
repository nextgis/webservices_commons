<template>
  <ul class="sidebar-menu">
    <li class="sidebar-menu__item"
      :class="{'active': activeItem === item.id }"
      v-for="item in items"
      >
        <a class="sidebar-menu__link" :href="item.link" v-html="item.text"></a>
    </li>
  </ul>
</template>

<script>
export default {
  name: 'SidebarMenu',
  props: {
    items: Array,
    activeItem: String
  },
  data() {
    return {};
  },
};
</script>

<style lang="styl" scoped>
  @require '~vuetify/src/stylus/settings/_colors';
  @require '~@nextgis_common/scss/custom-vuetify/_theme'
  @require '~@nextgis_common/scss/custom-vuetify/_variables'

  .sidebar-menu
    list-style-type: none;
    padding: 0;
    margin: 0;
    font-family: $heading-font-family;
    font-size: 14px;

    &__item
      position: relative;
      padding: 0 0 0 36px;
      margin: 0 0 12px;

      &.active
        &::before
          content: "";
          position: absolute;
          left: 0;
          top: .6em;
          width: 24px;
          height: 2px;
          background-color: $theme.primary;

    &__link
      text-decoration: none;
      border: 0;
      color: $material-theme.text.primary;

      &:hover
        color: $theme.primary;

  .sidebar-menu__item.active .sidebar-menu__link,
  .sidebar-menu__link:active,
  .sidebar-menu__link:focus
    color: $theme.primary;
    font-weight: 500;

</style>
