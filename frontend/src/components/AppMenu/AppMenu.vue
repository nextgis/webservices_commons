<template>
  <ul class="app-menu" :class="`app-menu--${view}`">
    <li class="app-menu__item"
      :class="{'active': activeItem === item.id }"
      v-for="item in items"
      :key = "item.id"
      >
        <a class="app-menu__link" :href="item.link" v-html="item.text"></a>
    </li>
  </ul>
</template>

<script>
export default {
  name: 'AppMenu',
  props: {
    items: Array,
    activeItem: String,
    view: {
      type: String, // 'vertical', 'horizontal'
      default: 'horizontal'
    },
  },
  data() {
    return {};
  },
};
</script>

<style lang="scss" scoped>

  .app-menu{
    list-style-type: none;
    padding: 0;
    margin: 0;
    font-family: $heading-font-family;
    font-size: 14px;

    &__link{
      text-decoration: none;
      border: 0;
      color: $text-base;

      &:hover{
        color: var(--v-primary-base);
      }
    }

    &--horizontal{
      display: flex;

      .app-menu__item{
        display: flex;
        align-items: center;
        padding: 0 12px;
        position: relative;

        &::after{
          position: absolute;
          content: "";
          left: 0;
          bottom: -1px;
          height: 3px;
          background: #0070c5;
          transition: max-width .4s;
          max-width: 0;
        }

        &:hover,
        &:focus,
        &:active{
            background-color: rgba(255,255,255,.24);
            color: #212121;
        }

        &.active{
          &::after{
            width: 100%;
            max-width: 200px;
          }

          &:hover{
            background-color: transparent;
          }
        }
      }
    }

    &--vertical{

      .app-menu__item{
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

        &.active .app-menu__link,
        .app-menu__link:active,
        .app-menu__link:focus{
          color: var(--v-primary-base);
          font-weight: 500;
        }
      }
    }
  }

</style>
