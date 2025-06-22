

/**
 * Represents a plant product.
 */
export default interface Plant {
    id:number,
    name: string,
    description: string,
    price: number,
    discount_percentage: number,
    discounted_price: number | null,
    stock_count: number,
    in_stock: boolean,
    rating: number,
    image: string,
}