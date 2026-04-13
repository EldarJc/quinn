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

        async login(payload) {
            this.error = null
            try {
                const response = await userService.login(payload);
                const { access_token, refresh_token } = response.data;
                localStorage.setItem('accessToken', access_token)
                localStorage.setItem('refreshToken', refresh_token);
                await this.fetchCurrentUser();
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
        async register(payload) {
            this.error = null
            try {
                const response = await userService.register(payload);
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
            } catch (error) {
                this.user = null

            }
        },

        async updateCurrentUser(payload) {
            const currentUser = this.user
            try{
                const {data} = await userService.updateCurrentUser(payload);
                this.user = data
            } catch (error) {
                this.error = error;
                this.user = currentUser
                throw error
            }
        },

        async updateUserImage(payload) {
            try{
                const {data} = await userService.updateUserImage(payload)
                this.user = data

            } catch (error) {
                this.error = error;
            }
        },

        async removeUserImage(){
            try{
                const {data} = await userService.removeUserImage()
                this.user = data
            } catch (error) {
                this.error = error;
            }
        },

        async fetchUser(username){
            try{
                const { data } = await userService.getUserProfile(username);
                return data
            } catch (error) {
                throw error;
            }

        }

    }
})