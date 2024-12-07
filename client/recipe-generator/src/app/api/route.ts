import axios from 'axios';

const getResponse = async (query: String) => {
  try {
    const res = await axios.post('http://127.0.0.1:5000/query', {
      query: query,
    });
    return res.data.response;
  } catch (error) {
    console.error('Error getting response:', error);
    throw new Error('Failed to get response');
  }
};

export default getResponse;
