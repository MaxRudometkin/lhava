# Project Name: RESTful API with Internal Orderbook

## Introduction

This project aims to develop a web-based REST API application in Python that serves two main functionalities: 
providing quotes based on live data from Vertex Protocol's orderbook and executing immediate fills for provided orders. 
The API will expose endpoints to interact with these functionalities, catering to users who require real-time market data and execution capabilities.

## Features

1. **Quote Endpoint:** Allows clients to request quotes by providing a ticker symbol and quantity. 
The response will include relevant information beyond just the price, 
ensuring users have comprehensive data to make informed decisions.

2. **Immediate Fill Endpoint:** Mocks the execution of an immediate fill, 
confirming or rejecting the order based on its validity upon arrival. 
This endpoint ensures that placed orders are validated before execution.

3. **Internal Orderbook:** Utilizes live data from Vertex Protocol's orderbook through a public and free API. 
The orderbook serves as the basis for generating quotes, and a background job is set up to regularly update this data.

## Implementation Details

### REST API

- The REST API is developed using Python, providing a lightweight and efficient web server.
- Two endpoints are exposed:
  - `/quote`: Accepts GET requests with parameters for ticker symbol and quantity, returning a quote with comprehensive information.
  - `/execute`: Accepts POST requests with order details, simulating immediate fill execution against the internal orderbook 
  - and responding with a JSON of pertinent details of the executed order for the client.

### Internal Orderbook

- The internal orderbook is populated with live data obtained from Vertex Protocol's using a public API.
- A background job fetches and updates this data regularly to ensure real-time information availability for generating quotes.

### Additional Considerations

- Error handling: Implement robust error handling mechanisms to handle various scenarios, such as invalid requests or failed executions.
- Authentication and authorization: Integrate authentication and authorization mechanisms to ensure secure access to the API endpoints.
- Logging: Implement logging to capture relevant events and debug information for monitoring and troubleshooting purposes.
- Assumptions: Feel free to make assumptions on the unclear parts of the case study, one of our job is making assumptions with limited knowledge we get from exchanges.

### Documentation for Vertex

You can find extensive documentation of Vertex in [Vertex Documentation](https://docs.vertexprotocol.com/developer-resources/api):

## Usage

To test the functionality of the application, follow these steps:

1. Send a live request to the `/quote` endpoint to get a quote for buying a certain amount of BTC.
2. Upon receiving the quote, attempt to mock-execute the order by sending a request to the `/execute` endpoint with the appropriate order details.

Please note that the actual execution of orders should be performed with caution, especially in live trading environments.
`/execute` endpoint should not interact with real exchange endpoints.

You can build and deploy the application using any method of your choice, whether it's through Docker or manual installation.

## Contributing

Contributions to improve and enhance the project are welcome. Please fork the repository, make changes, and submit a pull request for review.

## License

This project is licensed under the [MIT License](LICENSE), allowing for both personal and commercial use with proper attribution.

## Contact

For any inquiries or suggestions regarding the project, feel free to contact Lhava at sam@lhava.io or ata@lhava.io
