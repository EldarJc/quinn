import apiClient from '@/api/apiClient';

class UserService {

    login(username, password) {
        return apiClient
            .post('/auth/login', {username, password
            })
            .then(response => {
                if (response.data) {
                    return response.data;
                }
            });
    }

    logout() {
        return apiClient.post('/auth/logout')
    }

    register(username, firstName, lastName, email, password) {
        return apiClient.post('/auth/register', {
            username,
            first_name: firstName,
            last_name: lastName,
            email,
            password
        });
    }


    getCurrentUser() {
        return apiClient.get('/users/me');
    }

    updateCurrentUser(user) {
        return apiClient.put(`/users/me`, user);
    }

    getUserProfile(username) {
        return apiClient.get(`/users/${username}`)
    }

}


export default UserService;