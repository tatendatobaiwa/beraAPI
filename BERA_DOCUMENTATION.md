# Botswana Fuel Price API
## Technical Documentation for BERA

---

### Executive Summary

The Botswana Fuel Price API is a serverless REST API that automatically extracts the latest fuel prices from BERA's official press releases and provides them in a standardized JSON format. This API enables developers, businesses, and government systems to programmatically access current fuel pricing data.

---

## 🎯 **API Overview**

### Purpose
- Provide real-time access to official Botswana fuel prices
- Eliminate manual data entry and reduce errors
- Enable integration with business systems and applications
- Support transparency in fuel pricing information

### Data Source
- **Primary Source**: BERA Press Releases (https://www.bera.co.bw/media/press-releases)
- **Update Frequency**: Real-time (fetches latest data on each request)
- **Data Accuracy**: Directly sourced from official BERA announcements

---

## 🔗 **API Endpoint**

### Base URL
```
https://[api-gateway-url]/prices
```

### HTTP Method
```
GET /prices
```

### Authentication
- **Type**: None (Public API)
- **Rate Limiting**: Standard AWS API Gateway limits

---

## 📋 **API Response Format**

### Successful Response (HTTP 200)

```json
{
  "effectiveDate": "15th January 2024",
  "currency": "BWP",
  "prices": [
    {
      "product": "Retail Pump Price - Unleaded Petrol 93",
      "price": 14.50
    },
    {
      "product": "Retail Pump Price - Unleaded Petrol 95", 
      "price": 14.75
    },
    {
      "product": "Retail Pump Price - Diesel 50ppm",
      "price": 13.80
    },
    {
      "product": "Wholesale Price - Illuminating Paraffin",
      "price": 9.50
    }
  ],
  "sourceUrl": "https://www.bera.co.bw/media/press-releases/fuel-price-adjustment-jan-2024"
}
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `effectiveDate` | String | Date when the fuel prices become effective |
| `currency` | String | Currency code (always "BWP" for Botswana Pula) |
| `prices` | Array | List of fuel products and their prices |
| `prices[].product` | String | Full product name and category |
| `prices[].price` | Number | Price per litre in BWP |
| `sourceUrl` | String | Direct link to the BERA announcement |

### Error Responses

#### Service Unavailable (HTTP 503)
```json
{
  "error": "Data source (BERA) is currently unavailable."
}
```

#### Parsing Error (HTTP 500)
```json
{
  "error": "Failed to parse data from the source. The scraper may need an update."
}
```

---

## 🏗️ **Technical Architecture**

### Infrastructure
- **Platform**: AWS Lambda (Serverless)
- **API Gateway**: Amazon API Gateway
- **Runtime**: Python 3.11
- **Deployment**: Serverless Framework
- **Region**: us-east-1 (configurable)

### Dependencies
- **requests**: HTTP client for web scraping
- **beautifulsoup4**: HTML parsing and data extraction

### Performance Characteristics
- **Cold Start**: ~2-3 seconds
- **Warm Response**: ~500ms-1s
- **Timeout**: 30 seconds
- **Memory**: 128MB (default)

---

## 🔄 **Data Processing Workflow**

1. **Request Received**: API Gateway receives GET request
2. **Fetch Press Releases**: Lambda function requests BERA press releases page
3. **Find Latest Announcement**: Searches for most recent fuel price announcement
4. **Extract Data**: Parses announcement content using regex patterns
5. **Format Response**: Structures data according to API specification
6. **Return JSON**: Sends formatted response to client

### Data Extraction Logic

The API uses intelligent pattern matching to extract fuel prices:

```python
# Example patterns used
fuel_patterns = [
    ("Unleaded Petrol 93", r'petrol\s+93.*?(\d+\.\d+)'),
    ("Unleaded Petrol 95", r'petrol\s+95.*?(\d+\.\d+)'),
    ("Diesel 50ppm", r'diesel.*?(\d+\.\d+)'),
    ("Illuminating Paraffin", r'paraffin.*?(\d+\.\d+)')
]
```

---

## 🛡️ **Security & Compliance**

### Security Measures
- **HTTPS Only**: All communications encrypted
- **Input Validation**: Sanitized data processing
- **No Data Storage**: No persistent data storage
- **CORS Enabled**: Cross-origin requests supported

### Compliance
- **Data Source**: Official BERA publications only
- **No Personal Data**: No collection of user information
- **Public Information**: Only publicly available data

---

## 📊 **Monitoring & Reliability**

### Availability
- **Target Uptime**: 99.9%
- **Monitoring**: AWS CloudWatch
- **Alerting**: Automatic error detection

### Error Handling
- **Network Issues**: Graceful degradation
- **Website Changes**: Intelligent pattern matching
- **Rate Limiting**: Respectful scraping practices

### Logging
- **Request Logs**: API Gateway access logs
- **Function Logs**: CloudWatch Lambda logs
- **Error Tracking**: Detailed error messages

---

## 🔧 **Integration Guide**

### Sample Code Examples

#### JavaScript/Node.js
```javascript
const response = await fetch('https://[api-url]/prices');
const fuelData = await response.json();

console.log(`Petrol 93: ${fuelData.prices[0].price} BWP`);
```

#### Python
```python
import requests

response = requests.get('https://[api-url]/prices')
fuel_data = response.json()

for price in fuel_data['prices']:
    print(f"{price['product']}: {price['price']} BWP")
```

#### cURL
```bash
curl -X GET https://[api-url]/prices
```

### Integration Considerations
- **Caching**: Consider caching responses for 1-4 hours
- **Error Handling**: Implement retry logic for network errors
- **Rate Limiting**: Respect reasonable request frequencies
- **Fallback**: Have backup data sources if needed

---

## 📈 **Usage Analytics**

### Metrics Available
- Request count and frequency
- Response times and performance
- Error rates and types
- Geographic distribution of requests

### Reporting
- Real-time dashboards available
- Monthly usage reports
- Performance analytics

---

## 🚀 **Deployment Information**

### Current Status
- **Environment**: Production
- **Version**: 1.0.0
- **Last Updated**: [Deployment Date]
- **Health Status**: ✅ Operational

### Maintenance
- **Scheduled Maintenance**: None required
- **Updates**: Automatic deployment pipeline
- **Monitoring**: 24/7 automated monitoring

---

## 📞 **Support & Contact**

### Technical Support
- **Documentation**: This document
- **Issue Reporting**: [GitHub Issues URL]
- **Response Time**: 24-48 hours

### BERA Coordination
- **Data Source**: BERA Press Releases
- **Update Notifications**: Automatic detection
- **Compliance**: Follows BERA publication schedule

---

## 📋 **Appendices**

### Appendix A: Sample Responses
[Include various sample responses for different scenarios]

### Appendix B: Error Codes
[Detailed list of all possible error conditions]

### Appendix C: Testing Results
[Summary of comprehensive testing performed]

### Appendix D: Performance Benchmarks
[Detailed performance metrics and benchmarks]

---

**Document Version**: 1.0  
**Last Updated**: [Current Date]  
**Prepared for**: Botswana Energy Regulatory Authority (BERA)  
**Prepared by**: Fuel Price API Development Team