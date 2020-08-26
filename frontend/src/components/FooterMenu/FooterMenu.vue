<template>
  <ul class="footer-menu list-unstyled">
    <li class="footer-menu__item"
      v-for="(item, index) in items"
      :key="index">
      <a :href="item.link" target="_blank">{{ item.text }}</a>
    </li>
  </ul>
</template>

<script>
export default {

  name: 'FooterMenu',
  props: {
    items: Array,
    activeItem: String,
    view: {
      type: String, // 'vertical', 'horizontal'
      default: 'horizontal'
    },
  },
  data() {
    return {

    };
  },
};
</script>

<style lang="scss" scoped>

.footer-menu{
    margin-bottom: 0;

    &__item{
      display: inline-block;
      margin-left: 18px;
    }
}
</style>
