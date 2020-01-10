<template>
  <span class="self-link__container">
    <a class="anchor" :id="href"></a>
    <a class="self-link" :href="`#${href}`">
      <slot></slot>
    </a>
  </span>  
</template>

<script>
  export default{
    props: {
      href: String,
      text: String,
    },
    data() {
      return {}
    }
  };
</script>

<style lang="scss">

@import "~@nextgis_common/scss/variables/_variables";

.self-link,
.self-link:hover,
.self-link:active,
.self-link:focus{
  position: relative;
  color: inherit;
  text-decoration: none;
  border: 0;
}

.self-link:hover{
  &::before{
    font-family: 'Material Icons';
    font-weight: 400;
    font-style: normal;
    line-height: 1;
    letter-spacing: normal;
    text-transform: none;
    display: inline-block;
    font-size: 18px;
    color: $light-blue2;
    position: absolute;
    left: -24px;
    top: 50%;
    margin-top: -9px;
    content: 'link';
  }
}

</style>