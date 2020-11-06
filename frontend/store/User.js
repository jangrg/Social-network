
export const state = () => ({
  user: null,
})

export const mutations = {
  SET_LOGGED_USER(state, user) {
    state.user = user
  },

    RESET_USER(state) {
    state.user = undefined;
  },

}