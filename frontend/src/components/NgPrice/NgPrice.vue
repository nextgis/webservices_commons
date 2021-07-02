<template>
  <div class="ng-price">
    <template v-if="currencyComp.position === 'first'">
      <span class="ng-price__currency">{{currencyComp.symbol}}</span><span class="ng-price__amount">{{amount}}</span>
      <span v-if="monthly || yearly">{{suffix}}</span>
    </template>

    <template v-if="currencyComp.position === 'last'">
      <span class="ng-price__amount">{{amount}}</span>
      <span class="ng-price__currency">{{currencyComp.symbol}}</span><template v-if="monthly || yearly">{{suffix}}</template>
    </template>
  </div>
</template>

<i18n>
{
  "en": {
    "per_month": "/mo",
    "per_year": "/year"
  },
  "ru": {
    "per_month": "/мес.",
    "per_year": "/год"
  }
}
</i18n>

<script>
export default {
  name: 'NgPrice',
  props: {
    amount: {type: String},
    currency: {type: String},
    monthly: {type: Boolean},
    yearly: {type: Boolean},
  },
  data() {
    return {
      currencies: {
        'rub': {
          symbol: 'Р',
          position: 'last',
        },
        'usd': {
          symbol: '$',
          position: 'first'
        }
      }
    }
  },
  computed: {
    suffix(){
      if (this.monthly) return this.$t('per_month');
      if (this.yearly) return this.$t('per_year');;
    },
    currencyComp(){
      return this.currencies[this.currency];
    }
  }
};
</script>

<style lang="scss" scoped>
  @import "@nextgis_common/scss/variables/_variables.scss";

  .ng-price{
    font-family: $heading-font-family;

    &__amount{
      font-size: 1.25em;
      font-weight: 500;
      line-height: 1.2
    }
  }
</style>
