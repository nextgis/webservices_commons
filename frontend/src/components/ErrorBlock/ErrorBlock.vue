<template>
  <div class="error-block not-found">
    <div class="huge-text error-block__number">404</div>
    <h1 class="h2 error-block__title">{{ $t('message.notExist') }}</h1>
    <div class="error-block__descr"> {{ $t('message.checkLink') }} <a href="mailto:info@nextgis.com">{{ $t('message.letUsKnow') }}</a>.</div>
    <v-btn color="primary" x-large class="error-block__btn" onclick="history.back()">
      {{ $t('message.backBtn') }}
    </v-btn>
  </div>
</template>

<script>
export default {
  name: 'NotFound',
  i18n: {
    messages: {
      en: {
        message: {
          'notExist': 'Page does not exist',
          'checkLink': 'Check your link or',
          'letUsKnow': 'let us know',
          'backBtn': 'Go back'
        }
      },
      ru: {
        message: {
          'notExist': 'Страница не существует',
          'checkLink': 'Проверьте ссылку или',
          'letUsKnow': 'дайте нам знать',
          'backBtn': 'Вернуться назад'
        }
      }
    }
  },
}
</script>

<style lang="scss" scoped>
@import "~@nextgis_common/scss/variables/_variables";
@import "~@nextgis_common/scss/variables/_bootstrap_variables";

.error-block{
  font-size: $font-size-md;
  text-align: center;
  padding-top: 24px;

  @media (min-width: $screen-lg-min){
      font-size: $font-size-lg;
  }

  &__title{
    line-height: $line-height-base;
    margin: 15px -10px 10px;
    font-size: $font-size-h2-sm;
    text-transform: none;
    font-weight: normal;
    letter-spacing: normal;

    @media (min-width: $screen-sm-min){
      font-size: $font-size-h2-md;
      margin: 0 0 5px;
    }

    @media (min-width: $screen-md-min){
      font-size: $font-size-h2;
    }
  }

  &__number{
    font-size: 100px;
    font-weight: bold;
    color: #176FC1;
    line-height: 1;
    letter-spacing: 2px;

    @media (min-width: $screen-sm-min){
      font-size: 150px;
    }

    @media (min-width: $screen-md-min){
      font-size: 175px;
    }
  }
  &__descr{
    max-width: 650px;
    margin-left: auto;
    margin-right: auto;
  }
  &__btn{
    margin-top: 32px;
  }
}
</style>