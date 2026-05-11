import apiClient from '@/api/apiClient';

class TagService {
    getTags(page = 1, pageSize = 50) {
        return apiClient.get('/tags', {
            params: {page, page_size: pageSize}
        });
    }
}

export default TagService;