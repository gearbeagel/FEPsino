import { format, formatDistanceToNow, parse } from "date-fns";

export default function DisplayDate({ dateString }) {
    // Parse the date string into a valid Date object
    if (!dateString) {
        return null;
    }
    const date = parse(dateString, "dd-MM-yyyy HH:mm:ss", new Date());
    const formattedDate = format(date, "dd-MM-yyyy HH:mm:ss");

    return (
        <div>
            <span>{formattedDate}</span>
        </div>
    );
}