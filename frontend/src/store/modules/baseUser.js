import UserService from '../../services/UserService.js'

export const namespaced = true;

export const state = {
  isAuthenticated: false,
  user: {}
}

export const mutations = {
  SET_USER(state, user) {
    state.user = user;
  },
  SET_USER_IS_AUTHENTICATED(state, isAuthenticated) {
    state.isAuthenticated = isAuthenticated;
  }
}

export const actions = {
  fetchUser({ commit, dispatch }) {
    UserService.getUser()
      .then(user => {
        commit('SET_USER', user);
        commit('SET_USER_IS_AUTHENTICATED', user.isAuthenticated);
      })
      .catch(error => {
        console.error('There was a problem fetching user: ' + error.message);
      })
  }
}