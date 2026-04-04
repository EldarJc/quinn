import axios from 'axios';
import router from '@/router/routes';

const BASE_URL = 'http://localhost:8000';

const apiClient = axios.create({
    baseURL: BASE_URL,
    timeout: 10000,
})

apiClient.interceptors.request.use(
    (config) => {
        if (config.url === '/auth/refresh') {
            const refreshToken = localStorage.getItem('refreshToken');
            config.headers.Authorization = `Bearer ${refreshToken}`
            return config;
        }
        const token = localStorage.getItem('accessToken');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => Promise.reject(error)
);


apiClient.interceptors.response.use(
    (response) => response,
    async (error) => {
        const originalRequest = error.config;

        if (error.response?.status === 401 && !originalRequest._retry && originalRequest.url !== '/auth/login') {
            originalRequest._retry = true;

            try {
                const response = await apiClient.post(`/auth/refresh`);

                const { access_token, refresh_token } = response.data;

                localStorage.setItem('accessToken', access_token);
                localStorage.setItem('refreshToken', refresh_token);

                originalRequest.headers['Authorization'] = `Bearer ${access_token}`;
                return apiClient(originalRequest);
            } catch (error) {
                localStorage.removeItem('accessToken');
                localStorage.removeItem('refreshToken');
                await router.push('/login');
                return Promise.reject(error);

            }
        }

        const errorMessage = error.response?.data?.errors?.json ||
                            error.response?.data ||
                            error.json || error.message ||
                            'An unexpected error occurred'

        return Promise.reject(errorMessage)

    }
);

export default apiClient;