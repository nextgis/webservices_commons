import Vue from 'vue';

Vue.component(
  'NgButton', () => import('../components/NgButton/NgButton')
);

Vue.component(
  'NgSheet', () => import('../components/NgSheet/NgSheet')
);

Vue.component(
  'NgPrice', () => import('../components/NgPrice/NgPrice')
);