<template>
  <div class="locale-switcher">
      <v-menu top right close-on-click>
        <template v-slot:activator="{ on, attrs }">
          <span v-bind="attrs" v-on="on" class="cursor-pointer">
            {{currentLanguage}}
            <v-icon class="locale-switcher__icon">mdi-menu-down</v-icon>
          </span>
        </template>
        <ng-list :items="menuItems">
        </ng-list>
      </v-menu>
  </div>
</template>

<script>
import { mapState } from 'vuex';

export default {
  name: 'LocaleSwitcher',
  computed: {
    ...mapState(['baseApp']),
    currentLanguage() {
      return this.$i18n.locale === 'ru' ? 'Русский' : 'English'
    },
    menuItems(){
      return [
        {
          title: 'English',
          href: this.baseApp.currentPage.url.en
        },
        {
          title: 'Русский',
          href: this.baseApp.currentPage.url.ru
        },
      ]
    }
  }
};
</script>
