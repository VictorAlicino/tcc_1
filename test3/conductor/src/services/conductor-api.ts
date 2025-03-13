/*
    Endpoints for use with the Conductor API
*/

import {api} from './api';
import {conductorToken} from '@/models/conductor_models';

export const loginToConductor = async (email: string | null, google_sub: string | null): Promise<conductorToken> => {
    if (!email || !google_sub) throw new Error('Email and google_sub are required');
    const response = await api.post('/auth/conductor/login', {
        email,
        google_sub
    });
    if(response.status === 404) throw new Error('User not found');
    return response.data;
}