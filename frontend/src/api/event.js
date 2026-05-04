import apiClient from '@/api/apiClient';

class EventService {
    create(payload) {
        return apiClient.post('/events', payload);
    }

    getEvent(eventId, eventSlug) {
        return apiClient.get(`/events/${eventId}/${eventSlug}`);
    }

    updateImage(eventId, payload) {
        return apiClient.put(`/events/${eventId}/image`, payload);
    }

    deleteImage(eventId) {
        return apiClient.delete(`/events/${eventId}/image`);
    }


}

export default EventService;