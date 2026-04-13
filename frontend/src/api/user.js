import apiClient from '@/api/apiClient';

class UserService {

    login(payload) {
        return apiClient.post('/auth/login', payload);
    }

    logout() {
        return apiClient.post('/auth/logout');
    }

    register(payload) {
        return apiClient.post('/auth/register', payload);
    }


    getCurrentUser() {
        return apiClient.get('/users/me');
    }

    updateCurrentUser(user) {
        return apiClient.put(`/users/me`, user);
    }

    getUserProfile(username) {
        return apiClient.get(`/users/${username}`);
    }

    updateUserImage(payload) {
        return apiClient.put("/users/me/image", payload);
    }

    removeUserImage() {
        return apiClient.delete(`/users/me/image`);
    }

}


export default UserService;