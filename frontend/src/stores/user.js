import {defineStore} from "pinia"
import UserService from "@/api/user"

const userService = new UserService();

export const useUserStore = defineStore('user', {
    state: () => ({
        user: null,
        error: null,
    }),
    getters: {
        isAuthenticated: (state) => !!state?.user
    },

    actions: {

        async login({ username, password }) {
            this.error = null
            try {
                const data = await userService.login(username, password);
                const { access_token, refresh_token } = data;
                localStorage.setItem('accessToken', access_token)
                localStorage.setItem('refreshToken', refresh_token);
                await this.fetchCurrentUser();
                return data;
            } catch (error) {
                this.user = null
                this.error = error
                throw error
            }
        },
        async logout() {
            await userService.logout();
            localStorage.removeItem('accessToken');
            localStorage.removeItem('refreshToken');
            this.user = null
        },
        async register({ username, firstName, lastName, email, password }) {
            this.error = null
            try {
                const response = await userService.register(username, firstName, lastName, email, password);
                return response.data;
            } catch (error) {
                this.error = error;
                throw error;
            }
        },

        async fetchCurrentUser() {
            try {
                const {data} = await userService.getCurrentUser()
                this.user = data
            } catch (err) {
                this.user = null

            }
        },

    }
})