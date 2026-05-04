import apiClient from '@/api/apiClient';

class TagService {
    getTags(page, limit = 10) {
        return apiClient.get('/tags', {
            params: { page, limit }
        });
    }
}

export default TagService;