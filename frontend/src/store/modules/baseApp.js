export const namespaced = true;

export const state = {
  currentPage: null,
  config: null
}

export const mutations = {
  SET_CURRENT_PAGE(state, currentPage) {
    state.currentPage = currentPage;
  },
  SET_CONFIG(state, config) {
    state.config = config;
  }
}

// export const actions = {
//   init({ commit, dispatch }) {
//     console.log(window.menuActiveItem);
//     commit(SET_USER, window.menuActiveItem )
//   }
// }


export const actions = {
  init({ commit, dispatch }, config) {
    commit('SET_CURRENT_PAGE', window.currentPage);
    commit('SET_CONFIG', config);
  }
}