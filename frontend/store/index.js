import Vue from 'vue';
import axios from 'axios';

export const state = () => ({});

export const mutations = {
  SET_USER(state, user) {
    state.auth.user = user;
  },
  ADD_FOLLOWING(state, id) {
    state.auth.user.following.push(id);
  },
  REMOVE_FOLLOWING(state, id) {
    for (var i = 0; i < state.auth.user.following.length; i++) {
      if (state.auth.user.following[i] == id) {
        state.auth.user.following.splice(i, 1);
        break;
      }
    }
  }
}

export const actions = {

  async nuxtServerInit({ commit, state, dispatch }, { app, route, req }) {
    let token = this.$auth.getToken('local')
    if (token) {
      try {
        let response = await this.$axios.get('account/logged_user_data/', { headers: { 'Authorization': `${token}` } });
        commit('SET_USER', response.data.user)
      } catch (e) {
        console.log(e)
      }
      if (!this.$auth.$storage.getCookie("theme"))
        this.$auth.$storage.setCookie("theme", "light");
    }
  },

}