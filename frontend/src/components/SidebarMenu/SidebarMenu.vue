<template>
  <ul class="sidebar-menu">
    <li class="sidebar-menu__item"
      :class="{'active': activeItem === item.id }"
      v-for="item in items"
      :key = "item.id"
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

<style lang="scss" scoped>

  .sidebar-menu{
    list-style-type: none;
    padding: 0;
    margin: 0;
    font-family: $heading-font-family;
    font-size: 14px;

    &__item{
      position: relative;
      padding: 0 0 0 36px;
      margin: 0 0 12px;

      &.active{
        &::before{
          content: "";
          position: absolute;
          left: 0;
          top: .6em;
          width: 24px;
          height: 2px;
          background-color: var(--v-primary-base);
        }
      }
    }

    &__link{
      text-decoration: none;
      border: 0;
      color: $text-base;

      &:hover{
        color: var(--v-primary-base);
      }
    }
  }

  .sidebar-menu__item.active .sidebar-menu__link,
  .sidebar-menu__link:active,
  .sidebar-menu__link:focus{
    color: var(--v-primary-base);
    font-weight: 500;
  }

</style>
